# Data Quality Log

This document records data quality assessment results for both raw datasets.

---

## 1. Zillow ZHVI City-Level Dataset

**File:** data/raw/zillow_zhvi_city.csv
**Assessment date:** May 2026
**Assessed by:** Riya Dogra

### 1.1 Completeness

- Total rows (cities): ~10,000
- Monthly columns (2010-01 through 2023-12): 168
- City-years with at least one missing monthly value: ~8%, concentrated in smaller markets and years 2010-2012
- Cities with entirely missing data for a given year: <1%

### 1.2 Consistency

- Monthly column names follow consistent ISO 8601 date format (YYYY-MM-DD). No irregularities found.
- RegionType is uniformly 'city' across all rows.
- All state abbreviations are valid 2-letter USPS codes.

### 1.3 Accuracy

- ZHVI values are model-generated estimates.
- Outlier detection (>4 SD from state mean): 47 city-year observations flagged with zhvi_outlier_flag=True.
- No negative ZHVI values found.
- Maximum observed value: ~$3.2M (Atherton, CA).

### 1.4 Uniqueness

- RegionID is unique per row. No duplicates found.
- (RegionName, State) combination is unique per row.

### 1.5 Timeliness

- Data covers January 2000 through December 2023.

---

## 2. U.S. Census Bureau ACS 5-Year Income Dataset

**File:** data/raw/census_acs_income.csv
**Assessment date:** May 2026
**Assessed by:** Ella Ghiorghias

### 2.1 Completeness

- Total rows (place-year observations): ~450,000
- Rows with suppressed income (NaN): ~12% of all observations
- Suppression concentrated in places with fewer than 2,500 residents
- Places with NaN income in ALL years: ~2,100

### 2.2 Consistency

- FIPS codes are consistently zero-padded strings.
- Name column follows Census pattern consistently across all years.
- Year values are integers 2010-2023 with no gaps.

### 2.3 Accuracy

- ACS 5-year estimates have margins of error not included in this extract.
- For small places, confidence intervals can be wide (+/-20-40%).
- No income values above $500,000 found (max: ~$250,000).
- No zero income values found after sentinel replacement.

### 2.4 Uniqueness

- (state_fips, place_fips, year) is unique across all rows. No duplicates.

### 2.5 Timeliness

- Data covers survey years 2010-2023.
- The 2023 estimate reflects surveys 2019-2023.

---

## 3. Post-Integration Quality

**File:** data/integrated/housing_affordability.csv
**Assessment date:** May 2026

### 3.1 Match Rate

| Geography scope | Match rate |
|----------------|----------|
| All Zillow cities | ~62% (6,200 of ~10,000) |
| Cities with population > 25,000 | ~94% |
| Cities with population > 100,000 | ~99% |

### 3.2 Price-to-Income Ratio Plausibility Check

- National median ratio 2010: 3.2 (consistent with published housing research)
- National median ratio 2023: 5.1 (consistent with JCHS and Zillow published statistics)
- No negative ratios found.
- Ratios above 30 flagged: 12 city-years (ultra-luxury markets); retained.

### 3.3 Known Limitations

1. ACS income estimates are 5-year rolling averages matched to single-year ZHVI values, introducing timing noise.
2. ZHVI covers the 33rd-67th price percentile; Census income covers all households.
3. Fuzzy string matching may have a small number of incorrect matches despite manual review.
