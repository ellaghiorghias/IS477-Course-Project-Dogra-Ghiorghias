# Housing Affordability in U.S. Cities: Integrating Zillow ZHVI and Census Income Data (2010–2023)

## Contributors

- Riya Dogra (rdogra2@illinois.edu)
- Ella Ghiorghias (eghiorg2@illinois.edu)

---

## Summary

Housing affordability has emerged as one of the most pressing socioeconomic challenges in the United States. Over the past two decades, housing costs have risen dramatically in many metropolitan areas while wage growth has lagged behind, making it increasingly difficult for residents to afford homes near where they work or live.

This project builds an automated, end-to-end data pipeline that collects, integrates, cleans, and analyzes publicly available data on housing prices and household income across U.S. cities from 2010 to 2023. We combine the Zillow Home Value Index (ZHVI)—a monthly time-series housing price dataset covering thousands of U.S. cities—with median household income estimates from the U.S. Census Bureau’s American Community Survey (ACS) 5-Year Estimates (Table B19013). Integration is performed using shared geographic identifiers (city name, state) and temporal identifiers (year), after resolving naming inconsistencies between the two sources via fuzzy string matching.

Our central research questions are: (1) What trends exist in the relationship between housing prices and median household income across U.S. metropolitan areas from 2010 to 2023? (2) Which cities exhibit the largest increases in housing costs relative to income growth? (3) Are there regional geographic patterns in housing affordability trends? (4) Do incomes grow at a comparable rate to housing prices in large metropolitan areas?

Our analysis computes annual housing price-to-income ratios for matched cities and identifies areas where affordability has deteriorated most significantly. The data pipeline is fully automated and reproducible via a Snakemake workflow, enabling re-execution as new data become available.

---

## Data Profile

### Dataset 1: Zillow Home Value Index (ZHVI) — City Level

**Source:** Zillow Research Data Portal
**URL:** https://www.zillow.com/research/data/
**Direct download URL:** https://files.zillowstatic.com/research/public_csvs/zhvi/City_zhvi_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv
**File in repository:** data/raw/zillow_zhvi_city.csv
**Acquisition log:** data/raw/zillow_acquisition_log.txt
**Acquisition script:** scripts/acquire_zillow.py

**Structure and Content:**
The Zillow ZHVI dataset is provided as a single CSV file in wide time-series format. Each row represents one U.S. city or town, and columns include geographic metadata followed by one column per calendar month from January 2000 onward. Geographic columns include RegionID, SizeRank, RegionName (city name), RegionType, StateName, State (two-letter abbreviation), City, Metro, and CountyName. Monthly value columns follow a YYYY-MM-DD naming convention (e.g., 2010-01-31 through 2023-12-31).

The ZHVI measures the typical home value for single-family residences, condominiums, and co-ops in the 33rd–67th price percentile tier, smoothed and seasonally adjusted. It is a model-based estimate, not a raw transaction price, covering approximately 10,000+ U.S. cities and towns.

| Attribute | Value |
|-----------|-------|
| Format | CSV, wide format |
| Approx. size | ~50 MB uncompressed |
| Rows | ~10,000 (cities) |
| Columns | ~300+ (metadata + monthly values) |
| Temporal coverage | Jan 2000 – Dec 2023 (we use 2010–2023) |
| Geographic granularity | City / place level |

**Ethical and Legal Constraints:**
The ZHVI dataset is freely available for non-commercial research and educational use under Zillow’s Terms of Use. Commercial redistribution is prohibited. For this academic project, use is fully compliant. ZHVI values are model-generated estimates and should not be interpreted as verified transaction prices. Potential algorithmic bias in Zillow’s valuation model is acknowledged.

**Relation to Research Questions:**
Provides the housing cost component—the numerator of the price-to-income ratio.

---

### Dataset 2: U.S. Census Bureau ACS 5-Year Median Household Income — Place Level

**Source:** U.S. Census Bureau, American Community Survey (ACS) 5-Year Estimates
**API base URL:** https://api.census.gov/data/{year}/acs/acs5
**Variable:** B19013_001E — Median Household Income in the Past 12 Months (inflation-adjusted dollars)
**Geography:** All census-designated places (for=place:*&in=state:*)
**Years:** 2010–2023
**File in repository:** data/raw/census_acs_income.csv
**Acquisition log:** data/raw/census_acquisition_log.txt
**Acquisition script:** scripts/acquire_census.py

**Structure and Content:**
The Census dataset is retrieved via the Census Bureau’s public API and stored in tidy long format. Each row is a single city-year observation.

| Column | Description |
|--------|-------------|
| name | Full Census place name (e.g., "Chicago city, Illinois") |
| median_household_income | Median household income in USD; NaN = suppressed |
| state_fips | 2-digit numeric state FIPS code |
| place_fips | 5-digit numeric place FIPS code |
| year | Survey year (2010–2023) |

| Attribute | Value |
|-----------|-------|
| Format | CSV, long (tidy) format |
| Approx. size | ~120 MB uncompressed |
| Rows | ~450,000 (≈33,000 places × 14 years) |
| Columns | 5 |
| Temporal coverage | 2010–2023 |
| Geographic granularity | Census-designated place level |

**Ethical and Legal Constraints:**
Census data is in the public domain (U.S. Government work) and freely available for any use. No personally identifiable information is included. ACS 5-year estimates are rolling averages with margins of error not included in the API response; this statistical uncertainty is acknowledged. Smaller population places may have unreliable estimates. Proper attribution to the U.S. Census Bureau is provided throughout.

**Relation to Research Questions:**
Provides the income component—the denominator of the price-to-income ratio.

---

### Dataset Integration

The two datasets are linked by city name and year. Because naming conventions differ (Zillow: "Chicago"; Census: "Chicago city, Illinois"), a geographic crosswalk is built during cleaning using fuzzy string matching constrained within state, followed by manual review of ambiguous cases. The crosswalk is saved at data/raw/city_name_crosswalk.csv. The integrated output is data/integrated/housing_affordability.csv with columns: city, state, year, zhvi_annual_median, median_household_income, price_to_income_ratio.

This project maps to the **CRISP-DM** data lifecycle model: Business Understanding → Data Understanding → Data Preparation → Integration → Analysis → Reporting.

---

## Data Quality

Full quality assessment results are documented in docs/data_quality_log.md.

**Zillow ZHVI:** Approximately 8% of city-year observations have at least one missing monthly value, concentrated in smaller cities and pre-2012. No duplicate rows found. Outlier detection (values >4 SD from state mean) flagged a small number of implausible single-year jumps; these are retained but flagged with a zhvi_outlier_flag column.

**Census ACS Income:** Approximately 12% of place-year observations have suppressed income values (Census sentinel −666,666,666), replaced with NaN during acquisition. These suppressions are concentrated in places with fewer than 2,500 residents. No duplicate state_fips + place_fips + year combinations found.

**Post-integration:** After fuzzy matching, approximately 6,200 cities were successfully matched out of ~10,000 Zillow cities. Match rate for cities with populations above 25,000 exceeded 94%. Unmatched cities were primarily small towns with highly divergent naming conventions or present in only one dataset.

---

## Data Cleaning

All cleaning is implemented in scripts/clean_and_integrate.py.

**Zillow ZHVI:**
1. **Wide-to-long reshape:** pandas.melt() converted wide format (one column per month) to long format (one row per city-month), producing a date column and zhvi value column.
2. **Annual aggregation:** Monthly values aggregated to annual medians per city, aligning temporal granularity with Census income data. City-years with fewer than 6 valid monthly observations excluded.
3. **Column standardization:** RegionName renamed to city; StateName to state_name; extraneous columns dropped.
4. **Missing value handling:** City-years with majority-missing monthly values marked NaN rather than imputed, preserving data integrity.
5. **Outlier flagging:** City-years with ZHVI >4 SD from state mean flagged in zhvi_outlier_flag column but retained.

**Census ACS Income:**
1. **Name parsing:** The name field parsed via regex to extract a normalized city name, stripping legal suffixes ("city", "town", "village", "borough", "CDP") and state portion—necessary for geographic matching.
2. **Sentinel value verification:** The −666,666,666 suppression value confirmed replaced with NaN (handled in acquire_census.py).
3. **Type coercion:** median_household_income confirmed as integer; FIPS codes retained as zero-padded strings.
4. **Filtering:** Places with NaN income in more than 50% of available years excluded to prevent skewed trend analyses.

**Integration:**
1. **Fuzzy matching:** City names matched within state using rapidfuzz.process.extractOne() with an 88-point similarity threshold.
2. **Manual review:** ~340 ambiguous matches reviewed manually; decisions recorded in data/raw/city_name_crosswalk.csv.
3. **State constraint:** Matching restricted within state to prevent false cross-state matches (e.g., "Springfield, IL" vs. "Springfield, MO").
4. **Deduplication:** One-to-many matches resolved by retaining the highest-confidence match score.

---

## Findings

After integration and cleaning, annual price-to-income ratios were computed for 6,200+ matched cities across 2010–2023.

The national median price-to-income ratio rose from approximately 3.2 in 2010 to 5.1 in 2023—a 59% increase. This divergence accelerated sharply after 2020, coinciding with pandemic-era demand surges and historically low mortgage rates. The ten cities with the greatest affordability deterioration were concentrated in Florida (e.g., Naples, Cape Coral, Sarasota), the Mountain West (e.g., Boise, ID; Coeur d’Alène, ID), and coastal California, where ZHVI rose 150–250% while median income grew only 30–55%. Midwestern industrial cities showed the most stable or even declining ratios. A scatter analysis of annualized ZHVI growth vs. income growth revealed a weak positive correlation (r ≈ 0.22), confirming that price and income growth are largely decoupled. Visualizations are located in results/.

---

## Future Work

Several directions exist for extending this work. Incorporating the bottom-tier ZHVI would better capture affordability for first-time buyers and lower-income households. Building an automated annual refresh mechanism would keep the pipeline current as new ACS and ZHVI data are released. Adding contextual variables such as mortgage rates, property taxes, rental vacancy rates, and zoning laws could enable causal modeling beyond descriptive trends.

A key methodological lesson is that geographic identifier mismatches should be anticipated at the data acquisition stage. Future projects should prioritize shared standardized identifiers (e.g., FIPS codes via the HUD USPS ZIP-CBSA crosswalk) across datasets from the outset, rather than relying on post-hoc fuzzy name matching.

---

## Challenges

**Geographic naming mismatch** was the most significant technical challenge. Zillow uses short colloquial names while the Census API returns full legal names with type suffixes and state names appended. Simple string joins failed for a large share of cities. Fuzzy matching constrained within state, followed by manual review of ~340 ambiguous cases, resolved this but was time-intensive. The resulting crosswalk is fully documented.

**Dataset size** presented a version control challenge. The raw Zillow CSV (~50 MB) and Census CSV (~120 MB) exceed GitHub’s recommended per-file limit. Both files are tracked via Git LFS; acquisition scripts allow re-download from original sources, and SHA-256 checksums in acquisition logs enable integrity verification.

**Temporal granularity mismatch** between monthly ZHVI and annual ACS income required aggregation to annual medians. ACS “year” estimates are 5-year rolling averages, so comparisons should be interpreted as approximate trends rather than precise annual snapshots.

**Census data suppression** affected ~12% of place-year records. Excluding heavily suppressed cities from the integrated analysis may slightly undersample small and rural communities, which is acknowledged as a limitation in all findings.

---

## Reproducing

### Prerequisites
- Python 3.10+
- Git with Git LFS installed: git lfs install
- Optional: Free Census API key from https://api.census.gov/data/key_signup.html (recommended to avoid rate limits)

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/ellaghiorghias/IS477-Course-Project-Dogra-Ghiorghias.git
cd IS477-Course-Project-Dogra-Ghiorghias

# 2. Install dependencies
pip install -r requirements.txt

# 3. (Optional) Set Census API key
export CENSUS_API_KEY="your_key_here"

# 4. Run the complete pipeline
python run_all.py
#   -- OR using Snakemake --
snakemake --cores 1
```

Individual steps can also be run separately:

```bash
python scripts/acquire_zillow.py        # Download Zillow ZHVI data
python scripts/acquire_census.py        # Download Census ACS data
python scripts/clean_and_integrate.py   # Clean, reshape, and merge datasets
python scripts/analyze.py               # Compute ratios and generate visualizations
```

### Expected Outputs

| Path | Description |
|------|-------------|
| data/raw/zillow_zhvi_city.csv | Raw Zillow ZHVI data |
| data/raw/census_acs_income.csv | Raw Census ACS income data |
| data/raw/city_name_crosswalk.csv | Geographic name matching crosswalk |
| data/cleaned/zillow_zhvi_annual.csv | Annual ZHVI per city |
| data/cleaned/census_income_cleaned.csv | Cleaned Census income data |
| data/integrated/housing_affordability.csv | Merged dataset with price-to-income ratios |
| results/ | Visualizations and summary statistics |

---

## References

1. Zillow Research. (2024). *Zillow Home Value Index (ZHVI) Methodology*. https://www.zillow.com/research/methodology-neural-zhvi-32128/
2. U.S. Census Bureau. (2024). *American Community Survey 5-Year Estimates, Table B19013: Median Household Income*. https://api.census.gov/data/
3. U.S. Census Bureau. (2020). *Census Bureau API User Guide*. https://www.census.gov/data/developers/guidance/api-user-guide.html
4. McKinney, W. (2010). Data structures for statistical computing in Python. *Proceedings of the 9th Python in Science Conference*, 56–61.
5. The pandas development team. (2024). *pandas: powerful Python data analysis toolkit* (v2.x). https://doi.org/10.5281/zenodo.3509134
6. Bachmann, M., et al. (2021). *RapidFuzz: rapid fuzzy string matching in Python*. https://github.com/rapidfuzz/RapidFuzz
7. Mölder, F., et al. (2021). Sustainable data analysis with Snakemake. *F1000Research*, 10, 33. https://doi.org/10.12688/f1000research.29032.2

---

## License

- **Code:** MIT License (see LICENSE)
- **Data (Zillow ZHVI):** Subject to Zillow Terms of Use — non-commercial research use only
- **Data (Census ACS):** Public domain (U.S. Government work)
- **Documentation:** CC BY 4.0
