import os
import re
import hashlib

import pandas as pd
from rapidfuzz import process, fuzz


ZILLOW_RAW   = "data/raw/zillow_zhvi_city.csv"
CENSUS_RAW   = "data/raw/census_acs_income.csv"
ZILLOW_CLEAN = "data/cleaned/zillow_zhvi_annual.csv"
CENSUS_CLEAN = "data/cleaned/census_income_cleaned.csv"
CROSSWALK    = "data/raw/city_name_crosswalk.csv"
INTEGRATED   = "data/integrated/housing_affordability.csv"

MATCH_THRESHOLD = 88
MIN_MONTHLY     = 6
MAX_NULL_FRAC   = 0.50
STUDY_YEARS     = list(range(2010, 2024))


def makedirs_for(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)


def parse_census_name(name):
    m = re.match(
        r"^(.+?)(?:\s+(?:city|town|village|borough|CDP|municipality|township))?\s*,\s*(.+)$",
        name, re.IGNORECASE
    )
    if m:
        return m.group(1).strip(), m.group(2).strip()
    parts = name.rsplit(",", 1)
    return (parts[0].strip(), parts[1].strip()) if len(parts) == 2 else (name.strip(), "")


def clean_zillow():
    print("Loading Zillow ZHVI data...")
    df = pd.read_csv(ZILLOW_RAW)
    meta_cols = ["RegionID", "SizeRank", "RegionName", "RegionType",
                 "StateName", "State", "City", "Metro", "CountyName"]
    date_cols = [c for c in df.columns if re.match(r"\d{4}-\d{2}-\d{2}", c)]

    df_long = df[meta_cols + date_cols].melt(
        id_vars=meta_cols, value_vars=date_cols,
        var_name="date", value_name="zhvi"
    )
    df_long["date"] = pd.to_datetime(df_long["date"])
    df_long["year"] = df_long["date"].dt.year
    df_long = df_long[df_long["year"].isin(STUDY_YEARS)]

    def annual_median(g):
        valid = g["zhvi"].dropna()
        return valid.median() if len(valid) >= MIN_MONTHLY else float("nan")

    annual = (
        df_long.groupby(["RegionName", "StateName", "State", "year"])
        .apply(annual_median, include_groups=False)
        .reset_index(name="zhvi_annual_median")
    )
    annual = annual.rename(columns={
        "RegionName": "city",
        "StateName": "state_name",
        "State": "state_abbrev"
    })

    stats = (
        annual.groupby(["state_abbrev", "year"])["zhvi_annual_median"]
        .agg(["mean", "std"])
        .reset_index()
    )
    annual = annual.merge(stats, on=["state_abbrev", "year"], how="left")
    annual["zhvi_outlier_flag"] = (
        (annual["zhvi_annual_median"] - annual["mean"]).abs() > 4 * annual["std"]
    )
    annual.drop(columns=["mean", "std"], inplace=True)

    makedirs_for(ZILLOW_CLEAN)
    annual.to_csv(ZILLOW_CLEAN, index=False)
    print(f"  Saved {len(annual):,} rows to {ZILLOW_CLEAN}")
    return annual


def clean_census():
    print("Loading Census ACS income data...")
    df = pd.read_csv(CENSUS_RAW, dtype={"state_fips": str, "place_fips": str})
    df["state_fips"] = df["state_fips"].str.zfill(2)
    df["place_fips"] = df["place_fips"].str.zfill(5)

    parsed = df["name"].apply(parse_census_name)
    df["city_clean"] = [p[0] for p in parsed]
    df["state_name"] = [p[1] for p in parsed]
    df = df[df["year"].isin(STUDY_YEARS)].copy()

    null_frac = (
        df.groupby(["state_fips", "place_fips"])["median_household_income"]
        .apply(lambda s: s.isna().mean())
    )
    keep = null_frac[null_frac <= MAX_NULL_FRAC].index
    df = df[df.set_index(["state_fips", "place_fips"]).index.isin(keep)].copy()

    result = df[["city_clean", "state_name", "state_fips",
                 "place_fips", "year", "median_household_income"]]
    makedirs_for(CENSUS_CLEAN)
    result.to_csv(CENSUS_CLEAN, index=False)
    print(f"  Saved {len(result):,} rows to {CENSUS_CLEAN}")
    return result


def build_crosswalk(zillow_df, census_df):
    print("Building geographic name crosswalk...")
    from collections import defaultdict

    zillow_state_names = (
        zillow_df[["state_abbrev", "state_name"]]
        .drop_duplicates()
        .set_index("state_abbrev")["state_name"]
        .to_dict()
    )

    census_by_state = defaultdict(list)
    for _, row in census_df[["city_clean", "state_name"]].drop_duplicates().iterrows():
        census_by_state[row["state_name"]].append(row["city_clean"])

    rows = []
    for _, zrow in zillow_df[["city", "state_abbrev"]].drop_duplicates().iterrows():
        z_city = zrow["city"]
        z_state = zrow["state_abbrev"]
        z_state_name = zillow_state_names.get(z_state, "")
        candidates = census_by_state.get(z_state_name, [])
        if not candidates:
            rows.append({
                "zillow_city": z_city, "zillow_state": z_state,
                "census_city_clean": None, "census_state_name": z_state_name,
                "match_score": 0, "manual_review": False
            })
            continue
        match = process.extractOne(z_city, candidates, scorer=fuzz.WRatio)
        rows.append({
            "zillow_city": z_city,
            "zillow_state": z_state,
            "census_city_clean": match[0] if match else None,
            "census_state_name": z_state_name,
            "match_score": match[1] if match else 0,
            "manual_review": not match or match[1] < MATCH_THRESHOLD
        })

    crosswalk = pd.DataFrame(rows)
    makedirs_for(CROSSWALK)
    crosswalk.to_csv(CROSSWALK, index=False)
    auto = (~crosswalk["manual_review"] & crosswalk["census_city_clean"].notna()).sum()
    flagged = crosswalk["manual_review"].sum()
    print(f"  {auto:,} auto-matched | {flagged:,} flagged for manual review")
    return crosswalk


def integrate(zillow_df, census_df, crosswalk):
    print("Integrating datasets...")
    merged = zillow_df.merge(
        crosswalk[["zillow_city", "zillow_state", "census_city_clean",
                   "census_state_name", "match_score"]],
        left_on=["city", "state_abbrev"],
        right_on=["zillow_city", "zillow_state"],
        how="inner"
    )
    merged = merged[merged["census_city_clean"].notna()]

    final = merged.merge(
        census_df[["city_clean", "state_name", "year", "median_household_income"]],
        left_on=["census_city_clean", "census_state_name", "year"],
        right_on=["city_clean", "state_name", "year"],
        how="inner"
    )

    final["price_to_income_ratio"] = (
        final["zhvi_annual_median"] / final["median_household_income"]
    )

    out = (
        final[["city", "state_abbrev", "year", "zhvi_annual_median",
               "median_household_income", "price_to_income_ratio", "match_score"]]
        .rename(columns={"state_abbrev": "state"})
        .drop_duplicates(subset=["city", "state", "year"])
        .sort_values(["city", "state", "year"])
    )

    makedirs_for(INTEGRATED)
    out.to_csv(INTEGRATED, index=False)
    n_cities = out[["city", "state"]].drop_duplicates().shape[0]
    print(f"  Saved {len(out):,} rows | {n_cities:,} cities")
    return out


def main():
    print("=== Clean and Integrate Pipeline ===")
    zillow_df = clean_zillow()
    census_df = clean_census()
    crosswalk  = build_crosswalk(zillow_df, census_df)
    integrate(zillow_df, census_df, crosswalk)
    print("\nDone.")


if __name__ == "__main__":
    main()
