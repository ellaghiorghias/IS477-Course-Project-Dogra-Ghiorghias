
Status Report: Housing Affordability Data Pipeline

Project: Housing Price and Income Analysis Across U.S. Metropolitan Areas
Team: Riya Dogra & Ella Ghiorghias
Report Date:April 5, 2026


1. Overview of Progress

This is a summary of the housing affordability data pipeline project and where we are as of today. Since providing our original plan for the project we have obtained the necessary primary data and have created an organized archive of these datasets. Currently, we are engaged in data profiling and quality assurance activities for these datasets and are nearing completion of this work. Once data profiling and quality assurance have been completed, we will focus on data cleaning and integration prior to the following major stages of the data pipeline. We remain on track to meet the scheduled completion date of May 1, 2018.


2. Task-by-Task Update

Task 1: Data Acquisition (Riya) -Complete

Both datasets have been downloaded and  verified.

Acquisition scripts are located at `scripts/acquire_zillow.py` and `scripts/acquire_census.py`.


Task 2: Storage and Organization (Riya) -Complete

We have set up a directory framework and a file naming system for the repository.
At the present time, the root of the repository consists of two types of documents related to our project: documentation on the project itself (`README.md`, `ProjectPlan.md`) and acquisition scripts for getting data from two different sources (`acquire_zillow.py`, `acquire_census.py`).
As we continue to work on this project, we will categorize files into following subdirectories:

- `data/raw/` — stores untouched, unprocessed source files
- `data/cleaned/` — stores files after processing and cleaning
- `data/integrated/` — stores the merged final dataset
- `scripts/` — stores Python scripts for all stages of pipelines
- `docs/` — store documentation and associated metadata
- `results/` — stores visualizations or tables that are outputs of this project

Files saved in the repository will use the naming convention `{source}_{content}_{date}.csv`
(Example: `zillow_zhvi_city_2026-04-01.csv`) in order to facilitate reproduction and tracking of where the files originated from.
