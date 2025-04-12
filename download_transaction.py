import os
import requests
import zipfile
from io import BytesIO

# Constants
BASE_URL = "https://mempool-dumpster.flashbots.net/ethereum/mainnet/2025-03"
DEST_DIR = "transaction_data"
FILE_PATTERNS = [
    "2025-03-{day:02d}.csv.zip",
    "2025-03-{day:02d}_sourcelog.csv.zip"
]

# Loop through days in March (1 to 31)
for day in range(1, 32):
    subdir = f"{DEST_DIR}/03-{day:02d}"
    os.makedirs(subdir, exist_ok=True)

    for pattern in FILE_PATTERNS:
        filename = pattern.format(day=day)
        url = f"{BASE_URL}/{filename}"
        dest_zip_path = os.path.join(subdir, filename)

        try:
            print(f"Downloading {url}...")
            response = requests.get(url)
            if response.status_code == 200:
                with open(dest_zip_path, "wb") as f:
                    f.write(response.content)
                print(f"Saved zip to {dest_zip_path}")

                # Unzip the contents
                with zipfile.ZipFile(dest_zip_path, 'r') as zip_ref:
                    zip_ref.extractall(subdir)
                print(f"Unzipped contents to {subdir}")

                # Remove the zip file
                os.remove(dest_zip_path)
                print(f"Deleted zip file: {dest_zip_path}")
            else:
                print(f"Skipped {url} (status code: {response.status_code})")
        except Exception as e:
            print(f"Error handling {url}: {e}")
