import os
import requests
from zipfile import ZipFile
from io import BytesIO
from datetime import datetime, timedelta

# Output directory
output_dir = "data"
os.makedirs(output_dir, exist_ok=True)

# Define date range
start_date = datetime(2025, 3, 1)
end_date = datetime(2025, 3, 31)

# Base URL format
url_template = "https://bidarchive.relayscan.io/ethereum/mainnet/2025-03/{}_top.csv.zip"

# Loop over each day in March
current_date = start_date
while current_date <= end_date:
    date_str = current_date.strftime("%Y-%m-%d")
    url = url_template.format(date_str)
    print(f"Downloading: {url}")

    try:
        response = requests.get(url)
        response.raise_for_status()

        # Unzip in memory and save
        with ZipFile(BytesIO(response.content)) as z:
            z.extractall(output_dir)
            print(f"Extracted to: {output_dir}")
    except Exception as e:
        print(f"Failed to process {date_str}: {e}")

    current_date += timedelta(days=1)

print("All done.")
