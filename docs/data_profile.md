# **Source 1: US Census Dataset**
### **Table: Census Bureau API (ACS 5-Year, Table B19013)**

### **Structure, Content, Characteristics:**

The Census dataset has a tidy, long format, where each row represents a city-year observation.

**Columns:**

**name:** Full city name (e.g., “Chicago city, Illinois”)
- Used as a primary geographic identifier

**median_household_income:** Median household income (in U.S. dollars)
- Derived from ACS Table B19013
  
**state_fips:** Numeric code identifying the state
- Useful for precise joins and avoiding naming inconsistencies

**place_fips:** Unique identifier for each city/place
- Ensures consistent geographic matching

**year:**
- Year of the ACS estimate (2010–2023)

Additionally, (optional) metadata fields appear depending on extraction.

The Census dataset is stored in a cleaned, long-format structure with one row per city-year observation. Key variables include median household income, geographic identifiers (state and place FIPS codes), and year. This tidy structure will support efficient analysis, as it simplifies integration with housing price data after appropriate geographic standardization.

### **Location in Repository:** 
The Census dataset will be located under the `data/` folder, where it will be separated into "raw" and "cleaned" subgroups so that all of our steps and edits are evident for reproducibility. 

### **Ethical & Legal Constraints:**
The data is publicly available and free to use. We did not need any personally identifiable information, API keys, or other authentification to access the dataset. Ease and accessibility were two of our priorities while searching for potential targets.
There are a number of ethical considerations we should keep in mind while analyzing the data:
- Income estimates should not be interpreted as exact values; they can vary in actuality
- Margins of error should be acknowledged when drawing conclusions, so as to not wrongfully categorize samples of our population
- Smaller populations may generate misleading conclusions--when looking at any geographical area or subset, we will ensure that we are aware of the appropriate context
Legally, there are no restrictions on academic or analytical use. Proper attribution to the Census Bureau is "recommended", and we will treat this attribution as mandatory. 

### **Relation to Our Objective:**
This dataset provides the income component of housing affordability. It enables tracking income growth over time (2019–2023, or any other subset we choose to observe), as well as the comparison of income levels across cities. It directly answers one of our critical questions: How have household incomes changed across U.S. cities over time?

# **Source 2: Zillow Housing Price Index (ZHVI)**
### **Source URL: https://files.zillowstatic.com/research/public_csvs/zhvi/City_zhvi_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv**

### **Structure, Content, Characteristics:**

This dataset is also stored as a CSV file, but it uses a wide time-series format instead.

**Rows:** Each row represents a city

**Columns:**

**RegionName:** City name

**State:** State abbreviation

**Metro:** Associated metropolitan area

**Time-series columns:** Monthly values (e.g., 2010-01, 2010-02, ..., 2023-12)

### **Location in Repository:**
The Zillow dataset will be located under the `data/` folder alogn with the Census data, where it will be separated into "raw" and "cleaned" subgroups so that all of our steps and edits are evident for reproducibility. 

### **Ethical & Legal Constraints:**
This dataset is publicly available for research use, just like the Census dataset we extracted. Because we are subject to Zillow’s terms of use, we cannot cannot "redistribute commercially without permission", which is outside of the scope of our project. 
There are a number of ethical considerations we will have to keep in mind as well, namely:
- ZHVI values are estimates, not exact transaction prices--this is crucial to keep in mind as we attempt to integrate the datasets and draw conclusions. 
- Potential model bias should be acknowledged, as we've identified their history for automated data interpretation and exploitation in our Project Plan
- Avoid overinterpreting short-term fluctuations, since the dataset runs over a longer period of time

### **Relation to Our Objective:**
This dataset provides the housing cost component of the analysis. It enables the tracking of housing price trends over time, comparison of housing markets across cities, and measurement of price growth rates. With this dataset, we can directly answer this critical question: "How have housing prices changed across U.S. cities over time?"
