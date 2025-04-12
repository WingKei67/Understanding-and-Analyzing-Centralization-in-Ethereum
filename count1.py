import glob
import pandas as pd

# Pattern to match all relevant CSV files
file_pattern = "mev_boost_data/mevboost_*.csv"

# Get a list of all matching files
csv_files = glob.glob(file_pattern)

# Initialize tracking variables
min_slot = float('inf')
max_slot = float('-inf')

# Loop through files to find min and max slot
for file in csv_files:
    try:
        df = pd.read_csv(file, usecols=["slot"])
        file_min = df["slot"].min()
        file_max = df["slot"].max()
        min_slot = min(min_slot, file_min)
        max_slot = max(max_slot, file_max)
        print(f"{file}: min_slot={file_min}, max_slot={file_max}")
    except Exception as e:
        print(f"Error reading {file}: {e}")

print(f"\nOverall smallest slot: {min_slot}")
print(f"Overall largest slot: {max_slot}")
