Housing affordability is a major issue throughout many areas of the United States. We've seen rising costs for more than 20 years on an average basis for most parts of the country, making it increasingly difficult for individuals to afford housing options near where they work. Additionally, there were high levels of growth throughout the United States; therefore, a need exists to compare price changes for housing versus income changes in the household for cities and metropolitan regions across the United States at a later date.

This project will build an automated data pipeline that will collect, integrate, clean, and analyze data on housing prices and household income from various public sources. To do this, we will use housing price data available from Zillow and combine it with demographic and income data from the U.S. Census Bureau. In order to integrate these different datasets, we will use geographic identifiers, such as city and state, and temporal identifiers, such as year.

The following steps will need to be performed as part of this project: acquire data from reliable public sources, organize and store the raw data, assess data quality, clean and standardize the datasets, combine the datasets into a single unified dataset, and conduct exploratory analysis and visualization. Using Python and Pandas, we will compute various metrics, such as the ratio of housing prices to incomes, in order to analyze trends in housing affordability across different cities.

This project will result in an repeatable workflow able to automate the acquisition of data, as well as its cleaning, integration and analysis. The information derived from this project will highlight which cities have had the largest fluctuations in terms of housing affordability, along with a yearly comparison of the amount of income resulting from growth relative to the amount of increase in housing costs.

Team:
This project will be completed by Riya Dogra and Ella Ghiorghias. Riya and Ella will work together to complete the Data Lifecycle of acquisition, integration, cleaning, analysis, and documentation. Individual contributions to the project will appear in Git commit history of the project repository.
Riya (Data Acquisition and Workflow Automation) will acquire datasets from their respective sources, write scripts to retrieve and store acquired data, and implement the automated workflow to run the end-to-end analysis. Ella (Data Integration, Quality Assessment, and Analysis) will perform cleaning/standardization of acquired datasets, integrate datasets by means of common keys, and write scripts to conduct exploratory analysis and create visualizations. Both team members will collaborate in writing the documentation, interpreting the data, and creating the final project report to ensure reproducibility and a well-documented project.

Research or Business Questions:
The research project will answer the following questions:
1. What trends exist regarding the relationship between housing prices and median income across U.S. metropolitan areas over time? 
2. Which cities exhibit the most substantial increases in housing prices compared to median household income? 
3. Are there clear geographic patterns or relationships among different regions of the country when it comes to housing affordability trends? 
4. Do incomes grow at a similar pace as housing prices do in large metropolitan areas? 
This study's goal is to analyse, identify, and provide further details on selected historical trends in housing affordability by highlighting metropolitan areas where housing costs substantially exceed corresponding income levels.

Datasets:
Two main sources of data will be used for this project and both of them are publicly available reliable sources. They will provide complementary information and will be integrated based on geographic location and time period (the two attributes that are common to both datasets). 

Dataset 1: Zillow Housing Price Index (ZHVI)

Source:  Zillow Research Data : https://www.zillow.com/research/data/

We will use the  Time Series Housing Price Index Data from Zillow; The Housing Price Index (HPI) is an estimation tool developed by Zillow that tracks the price trends of homes across different cities and metropolitan areas of the US; The data provides a time series of estimates of housing prices. The data includes monthly or year-end HPI value estimates.

Key Variables
* City
* State
* Region or metropolitan area
* Date
* Housing price index value
Format CSV files available for download from the Zillow Research website.
In our Project , this dataset will be used to measure housing price trends across cities over time.

Dataset 2: U.S. Census Bureau Median Household Income Data

Source:  U.S. Census Bureau / American Community Survey https://data.census.gov

 The American Community Survey (ACS) provides demographic and economic information about U.S. households. For this project we will use median household income data by city or metropolitan area.
 
Key Variables
* City
* State
* Year
* Median household income
* Population
Format CSV files downloadable from the Census data portal.
In our Project, this dataset provides income data that will allow us to compare income growth with housing price changes.

Dataset Integration:
The datasets will be integrated using shared identifiers including:

1.City 
2.State 
3.Year or date

Because the Zillow dataset may be monthly while Census income data is yearly, the housing price data may be aggregated to yearly values to align the time scales between datasets. The resulting integrated dataset will contain:

1.City 
2.State 
3.Year 
4.Housing price index 
5.Median household income

This combined dataset will allow us to compute affordability metrics such as the housing price to income ratio and analyze trends across cities.

Our project will span the remainder of the spring semester. We are aiming to complete our data profile and quality assessment by Friday, April 3. This will prepare us for examination; sufficiently recording our raw data and remarking on any known flaws as we begin research. Our data cleaning will happen though out the following week, expecting completion by Friday, April 10—this step is designed to repair any of the deficiencies we discover throughout the first week. Missing values, outliers, and syntactic/semantic incongruencies will be resolved to the best of our ability. The findings, future work, and challenges we record throughout our project will be tabulated, tracked, and record by the end of the month: Friday, May 1. This will be out hard deadline for all required tasks/aspects, such as workflow automation and provenance, and reproducibility.

All associated details (references, reproduction, documentation, and concluding findings) will be completed in tandem with our final submission throughout the third and final phase ending on May 1. 

The data we have chosen does display several limitations: Zillow housing data is based on proprietary estimates instead of raw, verifiable transaction data like the government website. Because there are models interfering with true prices and rent scores by predicting and reshaping distributions instead of collecting and leaving raw datapoints, we may be liable to a small level of statistical deviation attributed to inaccurate datasets. 

The government Census website also has several flaws: for example, it tends to operate with survey-based results instead of complete, accurate counts of each household’s situation. 
Both websites suffer from the same problem of attempted shortcuts to mass data collection; we will have to consolidate these differences and aggregate numbers to use them both simultaneously.

The datasets also differ in their organization. Zillow defines all homes as single-family, condominium and co-operative homes with a county record. Unless specified, all series cover this segment of the housing stock. Census data, on the other hand, is organized within Census tracts instead of county boundaries. Inaccuracies could result if we attempt to inaccurately compare situations from two different locations, especially when so much of the American housing/property market is heavily demographically or socioeconomically divided.
 
Another common problem among the datasets is a lack of complete data representation. Both the geographical Census data and the Zillow website may be underrepresenting some of the country’s most vulnerable, impoverished areas: these are crucial for accurate representation. In order to maintain an ethically sound project, we will have to make sure that any samples taken from the data are randomly weighed and adequately representative of the country’s population.

There are some gaps within our project scope that we will have to navigate. Our primary question demands an involved analysis of household-level data and affordability measures, but the aforementioned geographic-level documentation may prevent us from accurately completing this goal. There are also many additional variables that we are currently missing that could be of greater use in answering this question (i.e., interest rates, credit history, household population, property taxes, and city taxes). Since we have only two members, we must use the two chosen datasets to complete our question. One way to resolve this gap is to limit our geographic consideration to a well-documented area. This would exchange inclusivity for accuracy: we could ensure a smaller, more indicative project regarding regional housing affordability. Gaps within our chosen metrics will also need to be resolved, as we need to consolidate both Zillow housing statistics with Government Census demographic variables. Our solutions to these gaps will be discussed in greater detail throughout our metadata and data documentation, as the two sources are spliced and altered to suit our needs.
