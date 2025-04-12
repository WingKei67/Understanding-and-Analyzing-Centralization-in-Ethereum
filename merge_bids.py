import pandas as pd

# Load the first CSV: enriched_data/merged_mevboost.csv
mevboost_df = pd.read_csv("enriched_data/merged_mevboost.csv")

# Keep only required columns
mevboost_df = mevboost_df[[
    "slot", "builder_pubkey", "block_number"
]]
mevboost_df["slot"] = mevboost_df["slot"].astype("int64")

# Load the second CSV: total_bids.csv
bids_df = pd.read_csv("total_bids.csv")

# Keep only required columns
bids_df = bids_df[[
    "slot", "slot_t_ms", "value", "block_hash", "builder_pubkey", "relay"
]]
bids_df["slot"] = bids_df["slot"].astype("int64")

# Perform a left merge on ['slot', 'builder_pubkey']
merged_df = pd.merge(
    mevboost_df,
    bids_df,
    how='left',
    on=['slot', 'builder_pubkey'],
)

# Load the builder mapping file
builder_df = pd.read_csv('builders_data.csv')

# Rename columns to make merging easier
builder_df = builder_df.rename(columns={
    'Builder Public Key': 'builder_pubkey',
    'Label': 'builder_label'
})

# Merge the data on builder_pubkey
merged_df = merged_df.merge(builder_df[['builder_pubkey', 'builder_label']], on='builder_pubkey', how='left')

# Save the updated result
merged_df.to_csv('merged_bids_labeled.csv', index=False)
print("Updated 'merged_bids.csv' with builder labels.")
