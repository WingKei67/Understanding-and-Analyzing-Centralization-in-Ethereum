import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load CSV
df = pd.read_csv("winning_bids_labeled.csv")

# Column names
value_col = 'value'         # in wei
builder_col = 'builder_label'
slot_col = 'slot'           # adjust if needed

# Convert wei to ETH
df['value_eth'] = pd.to_numeric(df[value_col], errors='coerce') / 1e18

# Filter valid entries
df = df.dropna(subset=['value_eth', builder_col, slot_col])
df = df[df['value_eth'] > 0]

# Aggregate ETH per builder per slot
eth_per_slot = df.groupby([builder_col, slot_col])['value_eth'].sum().reset_index()

# Compute Q1 and Q3 for each builder
quantiles = eth_per_slot.groupby(builder_col)['value_eth'].quantile([0.25, 0.75]).unstack()
quantiles.columns = ['q1', 'q3']

# Merge Q1/Q3 with original data
eth_merged = eth_per_slot.merge(quantiles, on=builder_col)

# Keep only values within Q1–Q3 range (remove extremes)
eth_filtered = eth_merged[
    (eth_merged['value_eth'] >= eth_merged['q1']) &
    (eth_merged['value_eth'] <= eth_merged['q3'])
]

# Plot setup
plt.figure(figsize=(14, 6))
sns.set(style="whitegrid")

# Assign unique colors
unique_builders = eth_filtered[builder_col].unique()
palette = sns.color_palette("husl", len(unique_builders))

# Boxplot (extremes removed)
sns.boxplot(
    data=eth_filtered,
    x=builder_col,
    y='value_eth',
    palette=dict(zip(unique_builders, palette)),
    linewidth=1,
    fliersize=0  # Hide outlier dots
)

# Labels and formatting
plt.xticks(rotation=45, ha='right')
plt.xlabel("Builder")
plt.ylabel("ETH per slot (within IQR)")
plt.title("MEV-Boost Payments per Slot (Extreme Values Removed)")

plt.tight_layout()
plt.show()
