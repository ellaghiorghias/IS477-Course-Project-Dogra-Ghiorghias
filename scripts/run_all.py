import subprocess
import sys


STEPS = [
    ("Acquiring Zillow ZHVI data",         ["python", "scripts/acquire_zillow.py"]),
    ("Acquiring Census ACS income data",    ["python", "scripts/acquire_census.py"]),
    ("Cleaning and integrating datasets",   ["python", "scripts/clean_and_integrate.py"]),
    ("Running analysis and visualizations", ["python", "scripts/analyze.py"]),
]


def run_step(description: str, command: list) -> None:
    print(f"\n{"="*60}")
    print(f"STEP: {description}")
    print(f"{"="*60}")
    result = subprocess.run(command, check=False)
    if result.returncode != 0:
        print(f"\nERROR: Step failed with return code {result.returncode}.")
        sys.exit(result.returncode)


if __name__ == "__main__":
    print("Housing Affordability Pipeline — Full Run")
    for desc, cmd in STEPS:
        run_step(desc, cmd)
    print("\nPipeline complete. Results are in the results/ directory.")
