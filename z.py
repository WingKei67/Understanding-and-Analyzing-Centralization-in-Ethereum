import pandas as pd

# Constants
GENESIS_TIME = 1606824023  # Beacon chain genesis time (in seconds)
SECONDS_PER_SLOT = 12

# Load CSV
df = pd.read_csv("winning_bids_labeled.csv")

# Compute slot timestamp in milliseconds
df['slot_timestamp_ms'] = (GENESIS_TIME + (df['slot']) * SECONDS_PER_SLOT) * 1000

# Calculate time in slot
df['time_in_slot_ms'] = df['timestamp_ms'] - df['slot_timestamp_ms']

# Save updated file
df.to_csv("winning_bids_with_time_in_slot.csv", index=False)

print("Done. New file saved as 'winning_bids_with_time_in_slot.csv'")
print("Median time_in_slot_ms:", df['time_in_slot_ms'].median())
