import pandas as pd
import glob
import os

# Define constants
DATA_DIR = 'data'
FILE_PATTERN = os.path.join(DATA_DIR, '2025-03-??_top.csv')
SLOT_MIN = 11163597
SLOT_MAX = 11386798
OUTPUT_FILE = 'total_bids.csv'

# Find all matching files
csv_files = glob.glob(FILE_PATTERN)

# Initialize a list to store DataFrames
filtered_dfs = []

# Loop through files and filter
for file in csv_files:
    df = pd.read_csv(file)
    if 'slot' in df.columns:
        df_filtered = df[(df['slot'] >= SLOT_MIN) & (df['slot'] <= SLOT_MAX)]
        filtered_dfs.append(df_filtered)

# Concatenate all filtered DataFrames
if filtered_dfs:
    total_df = pd.concat(filtered_dfs, ignore_index=True)
    total_df.to_csv(OUTPUT_FILE, index=False)
    print(f"Total records written to '{OUTPUT_FILE}': {len(total_df)}")
else:
    print("No matching records found.")
