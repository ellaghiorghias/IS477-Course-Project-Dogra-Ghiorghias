# Data Dictionary

This document describes all datasets used in the Housing Affordability project.

---

## data/raw/zillow_zhvi_city.csv

Raw Zillow Home Value Index data downloaded from Zillow Research.

| Column | Type | Description |
|--------|------|-------------|
| RegionID | integer | Unique Zillow region identifier |
| SizeRank | integer | Rank by market size (1 = largest) |
| RegionName | string | Short city name (e.g., "Chicago") |
| RegionType | string | Geography type (always "city" for this file) |
| StateName | string | Full state name (e.g., "Illinois") |
| State | string | Two-letter state abbreviation (e.g., "IL") |
| City | string | City name (mirrors RegionName) |
| Metro | string | Associated metro area name |
| CountyName | string | County the city is located in |
| YYYY-MM-DD | float | ZHVI estimate for that month in USD (NaN = missing) |

Notes:
- Columns from the 9th position onward are monthly date columns in YYYY-MM-DD format.
- ZHVI values represent the 33rd–67th percentile tier of single-family homes, condos, and co-ops.
- Values are model-based estimates, not verified transaction prices.

---

## data/raw/census_acs_income.csv

ACS 5-Year median household income data retrieved from the U.S. Census Bureau API.

| Column | Type | Description |
|--------|------|-------------|
| name | string | Full Census place name (e.g., "Chicago city, Illinois") |
| median_household_income | integer / NaN | Median household income in USD; NaN = suppressed by Census |
| state_fips | string | 2-digit zero-padded state FIPS code (e.g., "17" for Illinois) |
| place_fips | string | 5-digit zero-padded place FIPS code |
| year | integer | ACS survey year (2010–2023) |

Notes:
- Census sentinel value −666,666,666 (suppressed due to small sample) is replaced with NaN during acquisition.
- ACS 5-year estimates represent a rolling average; the "2023" estimate covers survey years 2019–2023.
- Margins of error are not included in this extract.

---

## data/raw/city_name_crosswalk.csv

Geographic name matching crosswalk built during the clean_and_integrate step.

| Column | Type | Description |
|--------|------|-------------|
| zillow_city | string | City name as it appears in the Zillow dataset |
| zillow_state | string | State abbreviation from the Zillow dataset |
| census_city_clean | string | Parsed city name from the Census dataset |
| census_state_name | string | State name from the Census dataset |
| match_score | float | Fuzzy match confidence score (0–100); scores below 88 were manually reviewed |
| manual_review | boolean | True if this match was reviewed and confirmed manually |

---

## data/cleaned/zillow_zhvi_annual.csv

Cleaned, reshaped, and annually aggregated Zillow data.

| Column | Type | Description |
|--------|------|-------------|
| city | string | Normalized short city name |
| state_name | string | Full state name |
| state_abbrev | string | Two-letter state abbreviation |
| year | integer | Year |
| zhvi_annual_median | float | Median of valid monthly ZHVI values for the year (USD) |
| zhvi_outlier_flag | boolean | True if value is more than 4 SD from the state mean for that year |

---

## data/cleaned/census_income_cleaned.csv

Cleaned Census ACS income data with parsed city names.

| Column | Type | Description |
|--------|------|-------------|
| city_clean | string | Parsed city name (legal suffix and state portion removed) |
| state_name | string | Parsed state name |
| state_fips | string | 2-digit state FIPS code |
| place_fips | string | 5-digit place FIPS code |
| year | integer | Year |
| median_household_income | integer / NaN | Median household income in USD |

---

## data/integrated/housing_affordability.csv

Final integrated dataset linking Zillow housing prices with Census income data.

| Column | Type | Description |
|--------|------|-------------|
| city | string | Matched city name |
| state | string | State abbreviation |
| year | integer | Year |
| zhvi_annual_median | float | Annual median ZHVI value in USD |
| median_household_income | integer | Median household income in USD |
| price_to_income_ratio | float | ZHVI divided by median_household_income |
| match_score | float | Fuzzy match confidence score from the crosswalk |

---

## results/summary_statistics.csv

Summary statistics computed during the analysis step.

| Column | Type | Description |
|--------|------|-------------|
| year | integer | Year |
| median_ratio_national | float | Median price-to-income ratio across all matched cities |
| mean_ratio_national | float | Mean price-to-income ratio across all matched cities |
| pct_cities_ratio_above_5 | float | Percentage of cities with ratio > 5 |
| pct_cities_ratio_above_10 | float | Percentage of cities with ratio > 10 |
