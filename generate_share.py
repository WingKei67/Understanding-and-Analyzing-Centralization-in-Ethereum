import pandas as pd

# Load the labeled CSV
df = pd.read_csv("winning_bids_labeled.csv")

# Drop rows missing slot or builder_label
df = df.dropna(subset=['builder_label', 'slot'])

# Group by builder and count number of slots (blocks) won
builder_slot_counts = df.groupby('builder_label')['slot'].count()

# Compute total slots and individual percentages
total_slots = builder_slot_counts.sum()
builder_percent = (builder_slot_counts / total_slots) * 100

# Sort by individual percentage (descending)
sorted_percent = builder_percent.sort_values(ascending=False)

# Build output with cumulative percentage
cumulative = 0.0
output = []

for builder, percent in sorted_percent.items():
    cumulative += percent
    output.append((builder, percent, cumulative))

# Save to CSV
output_df = pd.DataFrame(output, columns=['builder_label', 'slot_percentage', 'cumulative_percentage'])
output_df.to_csv("cumulative_builder_slot_share.csv", index=False)

print("Saved cumulative builder slot share to 'cumulative_builder_slot_share.csv'")
