
Status Report: Housing Affordability Data Pipeline

Project: Housing Price and Income Analysis Across U.S. Metropolitan Areas
Team: Riya Dogra & Ella Ghiorghias
Report Date:April 5, 2026


1. Overview of Progress

This is a summary of the housing affordability data pipeline project and where we are as of today. Since providing our original plan for the project we have obtained the necessary primary data and have created an organized archive of these datasets. Currently, we are engaged in data profiling and quality assurance activities for these datasets and are nearing completion of this work. Once data profiling and quality assurance have been completed, we will focus on data cleaning and integration prior to the following major stages of the data pipeline. We remain on track to meet the scheduled completion date of May 1, 2018.


2. Task-by-Task Update

Task 1: Data Acquisition (Riya) - Complete

Both datasets have been downloaded and  verified.

Acquisition scripts are located at `scripts/acquire_zillow.py` and `scripts/acquire_census.py`.


Task 2: Storage and Organization (Riya) - Complete

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

Task 3: Data Profile and Quality Assessment (Ella) — In Progress

We are currently in the process of doing data profiling. The two data sets we are looking at are being examined and documented for their structure and the amount of data inside them, as well as identifying any problems with the data. Below are our initial findings:

- The Zillow data set is in a wide format with one column representing every month; this means it will have to be transformed into a long format for analysis.
- There are also different geographic names being used by the two data sets, so integration will present challenges.
- The Census data has suppressions on small sample size city data that will have to be accounted for during the cleaning process.
- Because of this, we may have to look at different sorting categories (like Metro areas) to avoid city naming conventions.

We anticipate that the Data Profile and Data Quality will be completed relatively soon after submitting this report. The complete findings will be located in `docs/data_profile.md` and `docs/data_quality_log.md`.

3. Changes to the Project Plan

Our overall approach is consistent with the original project plan. There are a few minor edits that resulted from our preliminary examination of the data after aquiring the raw scripts. 

4. Challenges and Plans to Address Them

Challenge: Geographic identifier mismatch**

Upon preliminary review of both data sets indicates obvious differences in the way that each organization has named cities/metropolitan areas. Zillow has a naming structure that contains only city names themselves, whereas the Census Bureau has added qualifiers which identify whether it is a county, state, etc. Example of this name is "St. Louis City (MO)"; therefore a string join will not catch all matching city names as valid in either of these data sets.

Planned Approach to Eliminate the Differences: Fuzzy string matching will be performed using a Python Library to match on cities with a similarity score above an arbitrary threshold value for confidence and manually review any remaining ambiguous matches thereafter. The resulting matched city name crosswalk file will be saved as data/raw/city_name_crosswalk.csv and documented to ensure that the process can be reproduced.

 5. Individual Contribution Summaries

Riya Dogra
The main responsibility for this Milestone is acquiring the data. I did this by finding both source datasets for the acquisition scripts (acquire_zillow.py and acquire_census.py), testing them, and then committing raw data files to the git repo. I have also established the project directory structure and file naming conventions. Once the cleaning and integration pipeline is stable, I will start preparing for the automation workflow.

Ella Ghiorghias
As part of my milestone process, I have initiated data profiling and data quality assessment for both datasets. I am currently reviewing the structural layout and the completeness of data, along with formatting the datasets. I have been documenting initial findings for both datasets. I have identified the geographic naming mismatch as the main data quality issues to be addressed during the upcoming data cleaning. I will complete profile documentation soon, and then proceed to data cleansing and data integration over the next two weeks.

