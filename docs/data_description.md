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

The Census dataset is a tidy long-form data structure containing one row associated with a city-year observational unit. The median household income as well as geographical identifiers (state and place FIPS codes) and the year are all variables included in this dataset structure so it can more easily integrate with housing price data after appropriate geographic standardization.

### **Location in Repository:**
The Census dataset will be put into the 'data/` directory and have separate subgroups 'raw' and 'cleaned' to make apparent to any interested party all of our steps and modifications made to the data so as to facilitate replication.

### **Ethical and Legal Constraints:**
The data used in the project is also publicly available and can be accessed free of charge. We did not use any PII, API keys, or similar authentication methods to access any of this data. In addition, while researching potential target locations, our priority was ease and accessibility.

There are a number of ethical responsibilities to keep in mind while analyzing the data:
- Income estimates should not be construed as an exact figure as in actuality there is a great deal of variation.
- Acknowledge the presence of margins of error in making inferences from samples to the larger population.
The size of the population can create inaccurate assumptions; we must never lose sight of the geographical area or the demographic subset we are looking at, so we will take care that we are mindful of the appropriate context.

There are no legal restrictions regarding analytical or research purposes. The Census Bureau prefers to have their data cited properly as "recommended" (i.e., this requirement will be enforced by us).

### **Relation to Our Goal:**
This data set will provide the income factor contributing to housing affordability; it will allow us to analyze growth in household income for the last several years (2019 through 2023), or any way we wish to examine data.

It will also allow us to compare average incomes among cities throughout the United States at different times periods. This will address one of the main questions of our project's purpose: Have average household income levels changed in cities across America during recent times?

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

### Location of the Zillow dataset in the repository:
The Zillow dataset will be found in the `data/` directory and is organized in sub-folders called "raw" and "cleaned" so that each of our steps and edits are transparent to enabling replicability of our work.

### Legal and ethical limitations:
This data set is available to be used in research like the census data set that was pulled down by us. However, since we are subject to the terms of use established by Zillow we cannot redistribute this data for commercial purposes without prior approval which falls beyond the purview of this project.

There are several important ethical implications that we must consider, including the following:
1) The ZHVI values are only estimated values and not actual purchase prices; therefore, we need to keep this in mind while we integrate the two datasets and draw conclusions from them
2) Any model bias that we may encounter should be acknowledged as we identified possible sources of automated data interpretation and exploitation in our project plan
3) Over-interpreting short-term fluctuations in the data set will likely lead to erroneous conclusions, as we are looking over a considerable time period to analyze trends in sales activity.

### **How does our objective relate to this dataset?**
The analysis of housing costs provides a complete picture of our project's total analysis. As a result of this dataset, we can monitor trends in housing pricing over the years; compare various cities' housing markets; and measure how much prices have changed. With this information, one can respond to the critical question, "How have housing prices changed, over time, across the United States?"
