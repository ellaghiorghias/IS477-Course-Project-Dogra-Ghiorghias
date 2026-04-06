# **Source 1: US Census Dataset**
### **Table: Census Bureau API (ACS 5-Year, Table B19013)**

### **Structure, Content, Characteristics:**

The Census dataset has a tidy, long format, where each row represents a city-year observation.

Columns:

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

Additionally, (optional) metadata fields appear depending on extraction

### **Location in Repository:** 
The Census dataset will be located under the `data/` folder


### **Ethical & Legal Constraints:**

### **Relation to Our Objective:**

# **Source 2: Zillow Housing Price Index (ZHVI)**
### **Source URL: https://files.zillowstatic.com/research/public_csvs/zhvi/City_zhvi_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv**

### **Structure, Content, Characteristics:**

### **Location in Repository:**

### **Ethical & Legal Constraints:**

### **Relation to Our Objective:**
