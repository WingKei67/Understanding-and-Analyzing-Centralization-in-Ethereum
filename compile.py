import pandas as pd
import glob

# Get all files matching the pattern
csv_files = glob.glob("d?.csv")

# Read and concatenate the last 10000 rows from each file
combined_df = pd.concat([pd.read_csv(f).head(5000) for f in csv_files], ignore_index=True)

# Save to a new file (optional)
combined_df.to_csv("combined_test_files.csv", index=False)

print(f"Combined last 10000 rows from each of {len(csv_files)} files into 'combined_test_files.csv'")
