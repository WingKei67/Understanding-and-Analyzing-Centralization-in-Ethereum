import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load data
df = pd.read_csv("winning_bids_labeled.csv")

# Group by builder_label and relay to count bids
grouped = df.groupby(['builder_label', 'relay']).size().reset_index(name='count')

# Get total bids per builder
grouped['percentage'] = grouped.groupby('builder_label')['count'].transform(lambda x: x / x.sum() * 100)

# Get the relay with the highest share per builder
top_relay_per_builder = grouped.loc[grouped.groupby('builder_label')['percentage'].idxmax()]

# Sort for clearer plot
top_relay_per_builder = top_relay_per_builder.sort_values(by='percentage', ascending=False).reset_index(drop=True)

# Colors from a colormap
cmap = plt.get_cmap('tab20')  # Choose a visually distinct colormap
colors = [cmap(i % 20) for i in range(len(top_relay_per_builder))]

# Plot
plt.figure(figsize=(12, 6))
bars = plt.bar(top_relay_per_builder['builder_label'], top_relay_per_builder['percentage'], color=colors)


plt.xticks(rotation=45, ha='right')
plt.ylabel("Max Relay Share (%)")
plt.title("Top Relay Share of Winning Bids per Builder")
plt.tight_layout()
plt.show()
