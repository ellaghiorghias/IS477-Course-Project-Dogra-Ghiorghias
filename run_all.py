"""
run_all.py
End-to-end pipeline runner for the Housing Affordability project.
Executes all pipeline steps in order:
  1. Acquire Zillow ZHVI data
  2. Acquire Census ACS income data
  3. Clean and integrate datasets
  4. Analyze and produce visualizations
"""

import subprocess
import sys


STEPS = [
    ("Acquiring Zillow ZHVI data",         ["python", "scripts/acquire_zillow.py"]),
    ("Acquiring Census ACS income data",    ["python", "scripts/acquire_census.py"]),
    ("Cleaning and integrating datasets",   ["python", "scripts/clean_and_integrate.py"]),
    ("Running analysis and visualizations", ["python", "scripts/analyze.py"]),
]


def run_step(description: str, command: list) -> None:
    print(f"\n{'='*60}")
    print(f"STEP: {description}")
    print(f"{'='*60}")
    result = subprocess.run(command, check=False)
    if result.returncode != 0:
        print(f"\nERROR: Step failed with return code {result.returncode}.")
        print("Resolve the issue above and re-run, or run individual steps manually.")
        sys.exit(result.returncode)


if __name__ == "__main__":
    print("Housing Affordability Pipeline — Full Run")
    for desc, cmd in STEPS:
        run_step(desc, cmd)
    print("\nPipeline complete. Results are in the results/ directory.")
