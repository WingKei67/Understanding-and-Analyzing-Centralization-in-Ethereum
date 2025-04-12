import pandas as pd
import glob
import os

# Define the file pattern
file_pattern = 'enriched_data/mevboost_e?.csv'

# Get all matching file paths
csv_files = glob.glob(file_pattern)

# Sort the files (optional but useful if order matters)
csv_files.sort()

# Load and concatenate all CSVs
dfs = [pd.read_csv(file) for file in csv_files]
merged_df = pd.concat(dfs, ignore_index=True)

# Save to a new CSV file
output_path = 'enriched_data/merged_mevboost.csv'
merged_df.to_csv(output_path, index=False)

print(f"Merged {len(csv_files)} files into {output_path}")
