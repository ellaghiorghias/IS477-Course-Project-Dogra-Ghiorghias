Housing affordability is a major issue throughout many areas of the United States. We've seen rising costs for more than 20 years on an average basis for most parts of the country, making it increasingly difficult for individuals to afford housing options near where they work. Additionally, there were high levels of growth throughout the United States; therefore, a need exists to compare price changes for housing versus income changes in the household for cities and metropolitan regions across the United States at a later date.

This project will build an automated data pipeline that will collect, integrate, clean, and analyze data on housing prices and household income from various public sources. To do this, we will use housing price data available from Zillow and combine it with demographic and income data from the U.S. Census Bureau. In order to integrate these different datasets, we will use geographic identifiers, such as city and state, and temporal identifiers, such as year.

The following steps will need to be performed as part of this project: acquire data from reliable public sources, organize and store the raw data, assess data quality, clean and standardize the datasets, combine the datasets into a single unified dataset, and conduct exploratory analysis and visualization. Using Python and Pandas, we will compute various metrics, such as the ratio of housing prices to incomes, in order to analyze trends in housing affordability across different cities.

This project will result in an repeatable workflow able to automate the acquisition of data, as well as its cleaning, integration and analysis. The information derived from this project will highlight which cities have had the largest fluctuations in terms of housing affordability, along with a yearly comparison of the amount of income resulting from growth relative to the amount of increase in housing costs.

Team
This project will be completed by Riya Dogra and Ella Ghiorghias. Throughout the Data Lifecycle of acquisition, integration, cleaning, analysis and documentation, Riya and Ella will work together. Individual contributions to the project will appear in Git commit history of the project repository.

Riya (Data Acquisition and Workflow Automation) will acquire data from source(s), write script(s) to retrieve and store acquired data and implement the automated workflow to run the end-to-end analysis.

Ella (Data Integration/Quality Assessment/Analysis) will perform cleaning/standardization of acquired datasets, integrate datasets by means of common keys, write script(s) to conduct exploratory analysis and create visualizations.

Both team members will collaborate in writing the documentation, interpreting the data and creating the final project report to ensure reproducibility and well-documented project.


Research or Business Questions
The research project will answer the following questions:
1. What trends exist regarding the relationship between housing prices and median income across U.S. metropolitan areas over time? 
2. Which cities exhibit the most substantial increases in housing prices compared to median household income? 
3. Are there clear geographic patterns or relationships among different regions of the country when it comes to housing affordability trends? 
4. Do incomes grow at a similar pace as housing prices do in large metropolitan areas? 
This study's goal is to analyse, identify, and provide further details on selected historical trends in housing affordability by highlighting metropolitan areas where housing costs substantially exceed corresponding income levels.

Datasets
Two main sources of data will be used for this project and both of them are publicly available reliable sources. They will provide complementary information and will be integrated based on geographic location and time period (the two attributes that are common to both datasets). 


Dataset 1: Zillow Housing Price Index (ZHVI)
Source Zillow Research Data https://www.zillow.com/research/data/
Description Time Series Housing Price Index Data from Zillow; The Housing Price Index (HPI) is an estimation tool developed by Zillow that tracks the price trends of homes across different cities and metropolitan areas of the US; The data provides a time series of estimates of housing prices. The data includes monthly or year-end HPI value estimates.

Key Variables
* City
* State
* Region or metropolitan area
* Date
* Housing price index value
Format CSV files available for download from the Zillow Research website.
Purpose in the Project This dataset will be used to measure housing price trends across cities over time.

Dataset 2: U.S. Census Bureau Median Household Income Data
Source U.S. Census Bureau / American Community Survey https://data.census.gov
Description The American Community Survey (ACS) provides demographic and economic information about U.S. households. For this project we will use median household income data by city or metropolitan area.
Key Variables
* City
* State
* Year
* Median household income
* Population
Format CSV files downloadable from the Census data portal.
Purpose in the Project This dataset provides income data that will allow us to compare income growth with housing price changes.

Dataset Integration
The datasets will be integrated using shared identifiers including:
1.City 
2.State 
3.Year or date
Because the Zillow dataset may be monthly while Census income data is yearly, the housing price data may be aggregated to yearly values to align the time scales between datasets.
The resulting integrated dataset will contain:
1.City 
2.State 
3.Year 
4.Housing price index 
5.Median household income
This combined dataset will allow us to compute affordability metrics such as the housing price to income ratio and analyze trends across cities.

