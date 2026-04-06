
import hashlib
import os
import time
from datetime import datetime

import pandas as pd
import requests



# Years to collect (ACS 5-year estimates available from 2010 onward)
YEARS = list(range(2010, 2024))  # 2010–2023

# Census API variable:
#   B19013_001E = Median household income (estimate)
#   NAME        = Geographic name
VARIABLES = "NAME,B19013_001E"

# Geography: all "places" (cities, towns, CDPs) in the US
GEO = "for=place:*&in=state:*"

OUTPUT_DIR = "data/raw"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "census_acs_income.csv")
LOG_FILE = os.path.join(OUTPUT_DIR, "census_acquisition_log.txt")

# Optional API key (set via environment variable)
API_KEY = os.environ.get("CENSUS_API_KEY", "")

# Pause between requests to be respectful of the API (seconds)
REQUEST_DELAY = 0.5




def fetch_year(year: int, api_key: str) -> pd.DataFrame:
    """Fetch ACS 5-year median household income data for one year."""
    url = f"https://api.census.gov/data/{year}/acs/acs5"
    params = {
        "get": VARIABLES,
        "for": "place:*",
        "in": "state:*",
    }
    if api_key:
        params["key"] = api_key

    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()

    data = response.json()
    # First row is the header
    df = pd.DataFrame(data[1:], columns=data[0])
    df["year"] = year
    return df


def clean_frame(df: pd.DataFrame) -> pd.DataFrame:
    """Rename columns and do minimal type coercion."""
    df = df.rename(columns={
        "NAME": "name",
        "B19013_001E": "median_household_income",
        "state": "state_fips",
        "place": "place_fips",
    })
    df["median_household_income"] = pd.to_numeric(
        df["median_household_income"], errors="coerce"
    )
    # Sentinel value -666666666 means suppressed — replace with NaN
    df.loc[df["median_household_income"] < 0, "median_household_income"] = pd.NA
    return df


def compute_sha256(filepath: str) -> str:
    """Return the SHA-256 hex digest of a file."""
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def write_log(filepath: str, years: list, checksum: str) -> None:
    """Write acquisition metadata to a log file."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w") as f:
        f.write("Census ACS Acquisition Log\n")
        f.write("=" * 40 + "\n")
        f.write(f"Date acquired : {datetime.utcnow().isoformat()} UTC\n")
        f.write(f"Source        : Census Bureau API (ACS 5-Year, Table B19013)\n")
        f.write(f"Years fetched : {min(years)}–{max(years)}\n")
        f.write(f"Output file   : {OUTPUT_FILE}\n")
        f.write(f"SHA-256       : {checksum}\n")
    print(f"Log written to: {filepath}")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    all_frames = []

    for year in YEARS:
        print(f"Fetching {year}...", end=" ", flush=True)
        try:
            df = fetch_year(year, API_KEY)
            df = clean_frame(df)
            all_frames.append(df)
            print(f"{len(df)} rows")
        except requests.HTTPError as e:
            print(f"FAILED ({e}) — skipping {year}")
        time.sleep(REQUEST_DELAY)

    if not all_frames:
        print("ERROR: No data fetched. Check your internet connection or API key.")
        return

    combined = pd.concat(all_frames, ignore_index=True)
    combined.to_csv(OUTPUT_FILE, index=False)
    print(f"\nSaved {len(combined)} total rows to: {OUTPUT_FILE}")

    checksum = compute_sha256(OUTPUT_FILE)
    print(f"SHA-256: {checksum}")
    write_log(LOG_FILE, YEARS, checksum)
    print("Census acquisition complete.")


if __name__ == "__main__":
    main()
