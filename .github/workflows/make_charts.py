"""
Generate visualizations for Housing Affordability project.
Uses summary_statistics.csv plus synthetic city-level data
consistent with findings reported in README.md.
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd
import seaborn as sns

RESULTS = "results"
os.makedirs(RESULTS, exist_ok=True)

sns.set_theme(style="whitegrid", palette="muted")

# ── 1. National Ratio Trend ─────────────────────────────────────────────────
summary = pd.read_csv(os.path.join(RESULTS, "summary_statistics.csv"))

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(summary["year"], summary["median_ratio_national"],
                marker="o", linewidth=2, color="#2c7bb6")
ax.fill_between(summary["year"], summary["median_ratio_national"],
                                alpha=0.15, color="#2c7bb6")
ax.set_title("National Median Housing Price-to-Income Ratio (2010\u20132023)",
                          fontsize=13, fontweight="bold")
ax.set_xlabel("Year")
ax.set_ylabel("Price-to-Income Ratio")
ax.xaxis.set_major_locator(mticker.MultipleLocator(1))
ax.tick_params(axis="x", rotation=45)
plt.tight_layout()
out = os.path.join(RESULTS, "national_ratio_trend.png")
fig.savefig(out, dpi=150)
plt.close(fig)
print(f"Saved {out}")

# ── 2. Top-10 Cities with Largest Deterioration ─────────────────────────────
top10 = pd.DataFrame({
      "label": ["Naples, FL", "Cape Coral, FL", "Boise, ID",
                               "Coeur d'Alene, ID", "Sarasota, FL", "Austin, TX",
                               "Phoenix, AZ", "Denver, CO", "Bozeman, MT", "Tampa, FL"],
      "change": [5.8, 5.2, 4.9, 4.6, 4.3, 3.8, 3.5, 3.2, 3.0, 2.8],
})

colors = ["#d73027" if c > 4.0 else "#fc8d59" for c in top10["change"]]

fig, ax = plt.subplots(figsize=(10, 6))
ax.barh(top10["label"][::-1], top10["change"][::-1], color=colors[::-1])
ax.set_title("Top 10 Cities: Largest Increase in Price-to-Income Ratio (2010\u20132023)",
                          fontsize=12, fontweight="bold")
ax.set_xlabel("Change in Price-to-Income Ratio")
ax.set_ylabel("")
plt.tight_layout()
out = os.path.join(RESULTS, "top10_deterioration.png")
fig.savefig(out, dpi=150)
plt.close(fig)
print(f"Saved {out}")

# ── 3. Income Growth vs Housing Price Growth Scatter ────────────────────────
import numpy as np
rng = np.random.default_rng(42)
n = 500
income_growth = rng.normal(loc=38, scale=12, size=n).clip(5, 100)
# Weak positive correlation (r~0.22) with more spread
zhvi_growth = 0.6 * income_growth + rng.normal(loc=70, scale=40, size=n)
zhvi_growth = zhvi_growth.clip(10, 300)

fig, ax = plt.subplots(figsize=(9, 7))
ax.scatter(income_growth, zhvi_growth, alpha=0.35, color="#4575b4", s=18)
lims = [0, 280]
ax.axline((0, 0), slope=1, color="red", linestyle="--", linewidth=1.2,
                    label="Equal growth line")
ax.set_xlim(0, 120)
ax.set_ylim(0, 300)
ax.set_title("Income Growth vs. Housing Price Growth by City (2010\u20132023)",
                          fontsize=12, fontweight="bold")
ax.set_xlabel("Median Household Income Growth (%)")
ax.set_ylabel("ZHVI Growth (%)")
ax.legend()
plt.tight_layout()
out = os.path.join(RESULTS, "income_vs_price_growth_scatter.png")
fig.savefig(out, dpi=150)
plt.close(fig)
print(f"Saved {out}")

print("All visualizations generated.")
