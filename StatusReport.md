
# **Status Report: Housing Affordability Data Pipeline**

### Project: Housing Price and Income Analysis Across U.S. Metropolitan Areas
### Team: Riya Dogra & Ella Ghiorghias
### Report Date: April 5, 2026


## **1. Overview of Progress** ##

This is a summary of the housing affordability data pipeline project and where we are as of today. Since providing our original plan for the project we have obtained the necessary primary data and have created an organized archive of these datasets. Currently, we are engaged in data profiling and quality assurance activities for these datasets and are nearing completion of this work. Once data profiling and quality assurance have been completed, we will focus on data cleaning and integration prior to the following major stages of the data pipeline. We remain on track to meet the scheduled completion date of May 1, 2018.


## **2. Task-by-Task Update** ##

**Task 1: Data Acquisition** (Riya) - Complete

Both datasets have been downloaded and  verified.

Acquisition scripts are located at `scripts/acquire_zillow.py` and `scripts/acquire_census.py`.


**Task 2: Storage and Organization** (Riya) - Complete

We have set up a directory framework and a file naming system for the repository.
At the present time, the root of the repository consists of two types of documents related to our project: documentation on the project itself (`README.md`, `ProjectPlan.md`) and acquisition scripts for getting data from two different sources (`acquire_zillow.py`, `acquire_census.py`).
As we continue to work on this project, we will categorize files into following subdirectories:

- `data/raw/` - stores untouched, unprocessed source files
- `data/cleaned/` — stores files after processing and cleaning
- `data/integrated/` — stores the merged final dataset
- `scripts/` — stores Python scripts for all stages of pipelines
- `docs/` — store documentation and associated metadata
- `results/` — stores visualizations or tables that are outputs of this project

Files saved in the repository will use the naming convention `{source}_{content}_{date}.csv`
(Example: `zillow_zhvi_city_2026-04-01.csv`) in order to facilitate reproduction and tracking of where the files originated from.

**Task 3: Data Profile** (Ella) — Complete

The data profiles of both documents have been uploaded to the `docs/data_profile.md` file for storage. We have analyzed the raw formats of each dataset and observed their qualities, as well as any potential ethical or legal constraints associated with our sources. Our datasets relate directly to our questions, and we will proceed with them accordingly. 

**Task 4: Quality Assessment** (Ella) - In Progress

We are currently in the process of doing data profiling. The two data sets we are looking at are being examined and documented for their structure and the amount of data inside them, as well as identifying any problems with the data. Below are our initial findings:

- The Zillow data set is in a wide format with one column representing every month; this means it will have to be transformed into a long format for analysis.
- There are also different geographic names being used by the two data sets, so integration will present challenges.
- The Census data has suppressions on small sample size city data that will have to be accounted for during the cleaning process.
- Because of this, we may have to look at different sorting categories (like Metro areas) to avoid city naming conventions.

We anticipate that the Data Quality step will be completed relatively soon after submitting this report. The complete findings will be located in `docs/data_quality_log.md`.

## **3.a: Updated Project Timeline**

Our project will span the remainder of the spring semester. Because we have failed to complete our quality assessment by Friday, April 3, as originally planned, we will push this task back to the end of this week, April 10. Our original plan has allowed some leeway for spare time, so we are not concerned about this benchmark. Upon settling the final dataset samples, we will be able to move forward. 

Completing this task will prepare us for examination; sufficiently recording our raw data and remarking on any known flaws as we begin research. Our data cleaning will happen though out the following week, expecting completion by Friday, April 17 instead of April 10 - this step is designed to repair any of the deficiencies we discover. Missing values, outliers, and syntactic/semantic incongruencies will be resolved to the best of our ability. 

The findings, future work, and challenges we record throughout our project will be tabulated, tracked, and record by the end of the month: Friday, May 1. All of our progress will be recorded in line with the rubric provided. This date will be our hard deadline for all required tasks/aspects.

## **3.b: Changes to the Project Plan** ##

Our overall approach is consistent with the original project plan. There are a few minor edits that resulted from our preliminary examination of the data after aquiring the raw scripts. We plan to repair these setbacks by attending office hours and seeking additional help outside of class and our own abilities. 

## **4. Challenges and Plans to Address Them** ##

Challenge: Geographic identifier mismatch

Upon preliminary review of both data sets indicates obvious differences in the way that each organization has named cities/metropolitan areas. Zillow has a naming structure that contains only city names themselves, whereas the Census Bureau has added qualifiers which identify whether it is a county, state, etc. Example of this name is "St. Louis City (MO)"; therefore a string join will not catch all matching city names as valid in either of these data sets.

Planned Approach: Fuzzy string matching will be performed using a Python Library to match on cities with a similarity score above an arbitrary threshold value for confidence and manually review any remaining ambiguous matches thereafter. The resulting matched city name crosswalk file will be saved as data/raw/city_name_crosswalk.csv and documented to ensure that the process can be reproduced.

Challenge: Dataset size

GitHub imposes a soft 25 MB file size limite and a hard ~100 MB upper bound. It performs poorly with large, frequently updated datasets, making it impractical to store raw files like the U.S. Census Bureau ACS data and Zillow Research ZHVI data we plan to use. This creates challenges for version control, collaboration, and repository performance. 

Planned Approach: A common solution we can attempt is to store data externally (e.g., cloud storage like AWS S3, Google Cloud Storage, personal alternatives) and keep only scripts in GitHub. Alternatives include using the Git LFS download, APIs to fetch data, or storing cleaned, smaller subsets instead of full raw datasets. We will be verifying these solutions with our TA's and selecting the best possible way to move forward with the remainder of our analysis. 

## **5. Individual Contribution Summaries** ##

**Riya Dogra:**
The main responsibility for this Milestone is acquiring the data. I did this by finding both source datasets for the acquisition scripts (acquire_zillow.py and acquire_census.py), testing them, and then committing raw data files to the git repo. I have also established the project directory structure and file naming conventions. Once the cleaning and integration pipeline is stable, I will start preparing for the automation workflow.

**Ella Ghiorghias:**
As part of my milestone process, I have completed data profiling and started data quality assessment for both datasets. I am currently reviewing the structural layout and the completeness of data, along with the datasets' formatting. I have documented initial findings for both datasets and identified the geographic naming mismatches and dataset size discrepancies as the main data quality issues to be addressed during the upcoming data cleaning. I will proceed to data cleansing and data integration over the next two weeks with Riya's help. 

