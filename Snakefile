# Snakefile — Housing Affordability Pipeline
# Run the full pipeline with: snakemake --cores 1


rule all:
    input:
        "results/national_ratio_trend.png",
        "results/top10_deterioration.png",
        "results/income_vs_price_growth_scatter.png",
        "results/summary_statistics.csv"


rule acquire_zillow:
    output:
        "data/raw/zillow_zhvi_city.csv",
        "data/raw/zillow_acquisition_log.txt"
    shell:
        "python scripts/acquire_zillow.py"


rule acquire_census:
    output:
        "data/raw/census_acs_income.csv",
        "data/raw/census_acquisition_log.txt"
    shell:
        "python scripts/acquire_census.py"


rule clean_and_integrate:
    input:
        "data/raw/zillow_zhvi_city.csv",
        "data/raw/census_acs_income.csv"
    output:
        "data/cleaned/zillow_zhvi_annual.csv",
        "data/cleaned/census_income_cleaned.csv",
        "data/raw/city_name_crosswalk.csv",
        "data/integrated/housing_affordability.csv"
    shell:
        "python scripts/clean_and_integrate.py"


rule analyze:
    input:
        "data/integrated/housing_affordability.csv"
    output:
        "results/national_ratio_trend.png",
        "results/top10_deterioration.png",
        "results/income_vs_price_growth_scatter.png",
        "results/summary_statistics.csv"
    shell:
        "python scripts/analyze.py"
