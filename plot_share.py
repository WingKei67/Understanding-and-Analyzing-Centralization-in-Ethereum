import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV with builder_label, slot, and date
df = pd.read_csv("winning_bids_labeled.csv")

# Ensure correct data types
df['date'] = pd.to_datetime(df['date'])
df = df.dropna(subset=['slot', 'relay'])  # clean missing values

# Count number of blocks (slots) won by each builder per day
daily_block_counts = (
    df.groupby(['date', 'relay'])['slot']
    .count()
    .unstack(fill_value=0)
)

# Normalize to percentage of total slots per day
slot_share = daily_block_counts.div(daily_block_counts.sum(axis=1), axis=0) * 100

# Plot area chart
plt.figure(figsize=(16, 8))
slot_share.plot.area(stacked=True, figsize=(16, 8), linewidth=0)

plt.title("Slot Share Over Time by Relay", fontsize=18, weight='bold')
plt.ylabel("% of total slots")
plt.xlabel("")
plt.xticks(rotation=45)
plt.legend(title="Relays", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.grid(alpha=0.3)

# Optional: Save the plot
# plt.savefig("slot_share_chart.png", dpi=300)

plt.show()
