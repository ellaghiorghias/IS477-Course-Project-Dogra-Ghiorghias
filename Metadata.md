# **Integrated Metadata Summary**

This dataset serves as the primary output of the automated pipeline developed by Riya Dogra and Ella Ghiorghias. It facilitates the longitudinal analysis of housing affordability across the United States.

Name: *Housing Affordability in U.S. Cities (2010-2023)*

Description: A unified dataset merging city-level housing valuation indices with median household income estimates. It enables the calculation of price-to-income ratios to track affordability fluctuations.

Temporal Coverage: 2010 – 2023

Spatial Coverage: 6,200+ U.S. Cities

Format: CSV

# **Component Datasets**

The integrated product is derived from two high-authority public sources:

Dataset A: Zillow Home Value Index (ZHVI)

Source: Zillow Research Data

Role: Provides the time-series estimation of home values (HPI).

Key Variables: City, State, Metro Region, Date, and Housing Price Index Value.

Processing Note: Monthly Zillow data is aggregated into yearly values to maintain parity with Census reporting cycles.

Dataset B: U.S. Census Bureau Median Household Income
Source: American Community Survey (ACS) 5-Year Estimates

Role: Provides economic context via median household income and population figures.

Key Variables: City, State, Year, Median Household Income, and Population.

# **Data Schema & Integration Logic**
The datasets are integrated using a Composite Key strategy to ensure geographic and temporal alignment.

Field Name	Data Type	Description	Source
City	String	Standardized city name used as a primary join key.	Both
State	String	State abbreviation or name used to disambiguate cities.	Both
Year	Integer	The temporal anchor for the integration (2010-2023).	Both
ZHVI_Value	Numeric	The annual average of the Zillow Home Value Index.	Zillow
Median_Income	Numeric	The median household income for the specified city.	Census
Affordability_Ratio	Numeric	Computed metric: ZHVI_Value / Median_Income.	Derived
4. Administrative & Curation Metadata
Creators:

Riya Dogra: Data Acquisition and Workflow Automation.

Ella Ghiorghias: Data Integration, Quality Assessment, and Visualization.

Repository: GitHub: IS477-Course-Project-Dogra-Ghiorghias

Keywords: Housing Affordability, ZHVI, Census ACS, Price-to-Income Ratio, IS477.
