import pandas as pd

# Load the CSV
df = pd.read_csv("merged_bids_labeled.csv")

# Convert slot_t_ms to numeric (if needed)
df['slot_t_ms'] = pd.to_numeric(df['slot_t_ms'], errors='coerce')

# Drop rows with NaN slot_t_ms
df = df.dropna(subset=['slot_t_ms'])

# For each slot, find the row with the largest slot_t_ms
winning_bids_df = df.loc[df.groupby('slot')['slot_t_ms'].idxmax().values]

# Save to CSV
winning_bids_df.to_csv("winning_bids_labeled.csv", index=False)

print("Done. Saved as 'winning_bids_labeled.csv'")
