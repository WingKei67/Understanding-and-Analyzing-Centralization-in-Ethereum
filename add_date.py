import pandas as pd
import glob
import os

# Load the labeled bids
winning_bids_df = pd.read_csv('winning_bids_labeled.csv')

# Assume 'slot' is the column to match
slot_column = 'slot'  # Change this if your column name differs

# Create a new column for the matched date
winning_bids_df['matched_date'] = None

# Find all matching files
csv_files = glob.glob('data/2025-03-??_top.csv')

# Process each file
for file_path in csv_files:
    # Extract date from the filename
    date_str = os.path.basename(file_path).split('_')[0]
    
    # Read the file
    top_df = pd.read_csv(file_path)
    
    # Match based on slot and set date
    matched_slots = winning_bids_df[slot_column].isin(top_df[slot_column])
    winning_bids_df.loc[matched_slots, 'date'] = date_str

# Save the result
winning_bids_df.to_csv('winning_bids_labeled.csv', index=False)
