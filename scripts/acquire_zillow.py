
import hashlib
import os
import sys
from datetime import datetime

import requests



ZILLOW_URL = (
    "https://files.zillowstatic.com/research/public_csvs/zhvi/"
    "City_zhvi_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv"
)

OUTPUT_DIR = "data/raw"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "zillow_zhvi_city.csv")
LOG_FILE = os.path.join(OUTPUT_DIR, "zillow_acquisition_log.txt")




def compute_sha256(filepath: str) -> str:
    """Return the SHA-256 hex digest of a file."""
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def download_file(url: str, destination: str) -> None:
    """Download a file from url and write it to destination."""
    print(f"Downloading: {url}")
    response = requests.get(url, stream=True, timeout=60)
    response.raise_for_status()

    os.makedirs(os.path.dirname(destination), exist_ok=True)
    with open(destination, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    print(f"Saved to: {destination}")


def write_log(filepath: str, url: str, checksum: str) -> None:
    """Write acquisition metadata to a log file."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w") as f:
        f.write("Zillow ZHVI Acquisition Log\n")
        f.write("=" * 40 + "\n")
        f.write(f"Date acquired : {datetime.utcnow().isoformat()} UTC\n")
        f.write(f"Source URL    : {url}\n")
        f.write(f"Output file   : {OUTPUT_FILE}\n")
        f.write(f"SHA-256       : {checksum}\n")
    print(f"Log written to: {filepath}")


def main():
    try:
        download_file(ZILLOW_URL, OUTPUT_FILE)
    except requests.HTTPError as e:
        print(f"ERROR: Download failed — {e}")
        print(
            "The Zillow static file URL may have changed. "
            "Visit https://www.zillow.com/research/data/ to find the current link, "
            "then update ZILLOW_URL in this script."
        )
        sys.exit(1)

    checksum = compute_sha256(OUTPUT_FILE)
    print(f"SHA-256: {checksum}")
    write_log(LOG_FILE, ZILLOW_URL, checksum)
    print("Zillow acquisition complete.")


if __name__ == "__main__":
    main()
