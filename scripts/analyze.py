"""
analyze.py
Loads the integrated housing affordability dataset and produces:
  - results/national_ratio_trend.png : National median price-to-income ratio over time
  - results/top10_deterioration.png  : Top 10 cities with greatest ratio increase
  - results/income_vs_price_growth_scatter.png : Income growth vs ZHVI growth scatter
  - results/summary_statistics.csv   : Annual summary statistics
"""

import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns

INTEGRATED = "data/integrated/housing_affordability.csv"
RESULTS    = "results"

sns.set_theme(style="whitegrid", palette="muted")


def makedirs():
    os.makedirs(RESULTS, exist_ok=True)


def load_data():
    print("Loading integrated dataset...")
    df = pd.read_csv(INTEGRATED)
    df = df.dropna(subset=["zhvi_annual_median","median_household_income","price_to_income_ratio"])
    print(f"  {len(df):,} rows, {df[["city","state"]].drop_duplicates().shape[0]:,} cities")
    return df


def plot_national_trend(df):
    print("Generating national ratio trend chart...")
    annual = df.groupby("year")["price_to_income_ratio"].median().reset_index()
    annual.columns = ["year","median_ratio"]

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(annual["year"], annual["median_ratio"], marker="o", linewidth=2, color="#2c7bb6")
    ax.fill_between(annual["year"], annual["median_ratio"], alpha=0.15, color="#2c7bb6")
    ax.set_title("National Median Housing Price-to-Income Ratio (2010-2023)", fontsize=14, fontweight="bold")
    ax.set_xlabel("Year")
    ax.set_ylabel("Price-to-Income Ratio")
    ax.xaxis.set_major_locator(plt.MultipleLocator(1))
    ax.xaxis.set_tick_params(rotation=45)
    plt.tight_layout()
    out = os.path.join(RESULTS, "national_ratio_trend.png")
    fig.savefig(out, dpi=150)
    plt.close(fig)
    print(f"  Saved {out}")


def plot_top10_deterioration(df):
    print("Generating top-10 deterioration chart...")
    pivot = df.pivot_table(index=["city","state"], columns="year", values="price_to_income_ratio")

    # Only keep cities with data in both 2010 and 2023
    pivot = pivot.dropna(subset=[2010, 2023])
    pivot["change"] = pivot[2023] - pivot[2010]
    top10 = pivot.nlargest(10, "change")[["change",2010,2023]].reset_index()
    top10["label"] = top10["city"] + ", " + top10["state"]

    fig, ax = plt.subplots(figsize=(10, 6))
    colors = ["#d73027" if c > 5 else "#fc8d59" for c in top10["change"]]
    bars = ax.barh(top10["label"][::-1], top10["change"][::-1], color=colors[::-1])
    ax.set_title("Top 10 Cities: Largest Increase in Price-to-Income Ratio (2010-2023)",
                 fontsize=13, fontweight="bold")
    ax.set_xlabel("Change in Price-to-Income Ratio")
    ax.set_ylabel("")
    plt.tight_layout()
    out = os.path.join(RESULTS, "top10_deterioration.png")
    fig.savefig(out, dpi=150)
    plt.close(fig)
    print(f"  Saved {out}")


def plot_income_vs_price_growth(df):
    print("Generating income vs price growth scatter...")
    base = df[df["year"].isin([2010, 2023])]
    piv_zhvi   = base.pivot_table(index=["city","state"], columns="year", values="zhvi_annual_median")
    piv_income = base.pivot_table(index=["city","state"], columns="year", values="median_household_income")

    growth = pd.DataFrame({
        "zhvi_growth":   (piv_zhvi[2023]   / piv_zhvi[2010]   - 1) * 100,
        "income_growth": (piv_income[2023] / piv_income[2010] - 1) * 100,
    }).dropna()

    # Remove extreme outliers for display
    growth = growth[(growth["zhvi_growth"] < 500) & (growth["income_growth"] < 200)]

    fig, ax = plt.subplots(figsize=(9, 7))
    ax.scatter(growth["income_growth"], growth["zhvi_growth"],
               alpha=0.35, s=20, color="#4575b4")
    ax.axline((0,0), slope=1, color="red", linestyle="--", linewidth=1.2, label="Equal growth line")
    ax.set_title("Income Growth vs. Housing Price Growth by City (2010-2023)",
                 fontsize=13, fontweight="bold")
    ax.set_xlabel("Median Household Income Growth (%)")
    ax.set_ylabel("ZHVI Growth (%)")
    ax.legend()
    plt.tight_layout()
    out = os.path.join(RESULTS, "income_vs_price_growth_scatter.png")
    fig.savefig(out, dpi=150)
    plt.close(fig)
    print(f"  Saved {out}")


def save_summary_stats(df):
    print("Computing summary statistics...")
    summary = df.groupby("year").agg(
        median_ratio_national=("price_to_income_ratio","median"),
        mean_ratio_national=("price_to_income_ratio","mean"),
        n_cities=("city","nunique"),
    ).reset_index()
    summary["pct_cities_ratio_above_5"]  = df.groupby("year").apply(
        lambda g: (g["price_to_income_ratio"] > 5).mean() * 100).values
    summary["pct_cities_ratio_above_10"] = df.groupby("year").apply(
        lambda g: (g["price_to_income_ratio"] > 10).mean() * 100).values

    out = os.path.join(RESULTS, "summary_statistics.csv")
    summary.to_csv(out, index=False)
    print(f"  Saved {out}")
    print(summary.to_string(index=False))


def main():
    makedirs()
    df = load_data()
    plot_national_trend(df)
    plot_top10_deterioration(df)
    plot_income_vs_price_growth(df)
    save_summary_stats(df)
    print("\nAnalysis complete.")


if __name__ == "__main__":
    main()
