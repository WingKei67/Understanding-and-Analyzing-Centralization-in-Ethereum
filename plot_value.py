import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

# Load dataset
df = pd.read_csv("winning_bids_labeled.csv")

# Ensure 'value' is numeric and drop rows with missing values
df['value'] = pd.to_numeric(df['value'], errors='coerce') / 1e18  # Convert wei to ETH
df = df.dropna(subset=['builder_label', 'value'])
overall_mean = df['value'].mean()
print(df['value'].std())
print(f"Overall mean block value across all builders: {overall_mean:.4f} ETH")

# Group by builder_label and compute mean value
mean_values = df.groupby('builder_label')['value'].mean().sort_values(ascending=False)

# Set color map
num_labels = len(mean_values)
colors = cm.get_cmap('tab20b', num_labels)(np.arange(num_labels))

# Plot
plt.figure(figsize=(14, 6))
bars = plt.bar(mean_values.index, mean_values.values, color=colors, edgecolor='black')

plt.title("Mean Block Value by Builders", fontsize=16, weight='bold')
plt.ylabel("Mean Value (ETH)")
plt.xlabel("Builder Label")
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()

# Optional: Save the figure
# plt.savefig("mean_block_value_by_builder.png", dpi=300)

plt.show()
