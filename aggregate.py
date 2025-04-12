import pandas as pd
import os
import glob

# Define the directory and file pattern
data_dir = 'data'
file_pattern = os.path.join(data_dir, '2025-*-*_top.csv')
file_paths = glob.glob(file_pattern)

# Container for aggregated DataFrames
aggregated_dfs = []

for file_path in file_paths:
    try:
        df = pd.read_csv(file_path)
        if 'slot' in df.columns and 'value' in df.columns:
            # Ensure value is numeric
            df['value'] = pd.to_numeric(df['value'], errors='coerce')
            df = df.dropna(subset=['slot', 'value'])

            # Get the highest value per slot
            idx = df.groupby('slot')['value'].idxmax()
            df_max = df.loc[idx]

            # Extract date from filename
            filename = os.path.basename(file_path)
            date_str = filename.split('_')[0]
            df_max['date'] = date_str

            aggregated_dfs.append(df_max)
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

# Combine all into one DataFrame and save
if aggregated_dfs:
    result_df = pd.concat(aggregated_dfs, ignore_index=True)
    result_df.to_csv('winning_bids.csv', index=False)
    print("Aggregation complete. Output saved to 'winning_bids.csv'.")
else:
    print("No data was aggregated.")
