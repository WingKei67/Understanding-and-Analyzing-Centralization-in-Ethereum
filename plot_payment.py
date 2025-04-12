import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV that contains builder_label, value, and date
df = pd.read_csv("winning_bids_labeled.csv")

# Ensure correct data types
df['value'] = pd.to_numeric(df['value'], errors='coerce')
df['date'] = pd.to_datetime(df['date'])

# Group by date and builder_label, summing up the values
daily_value_share = (
    df.groupby(['date', 'relay'])['value']
    .sum()
    .unstack(fill_value=0)
)

# Normalize to percentage share per day
percentage_df = daily_value_share.div(daily_value_share.sum(axis=1), axis=0) * 100

# Plot area chart
plt.figure(figsize=(16, 8))
percentage_df.plot.area(stacked=True, figsize=(16, 8), linewidth=0)

plt.title("MEV-Boost Payment Share Over Time by Relay", fontsize=18, weight='bold')
plt.ylabel("% of ETH distributed")
plt.xlabel("")
plt.xticks(rotation=45)
plt.legend(title="Relays", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.grid(alpha=0.3)

# Save the figure if needed
# plt.savefig("mev_boost_share.png", dpi=300)

plt.show()
