import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm

# Load the dataset
df = pd.read_csv("total_bids.csv")

# Ensure numeric and drop missing values
df["received_at_ms"] = pd.to_numeric(df["received_at_ms"], errors="coerce")
df["timestamp_ms"] = pd.to_numeric(df["timestamp_ms"], errors="coerce")
df = df.dropna(subset=["received_at_ms", "timestamp_ms", "relay"])

# Compute latency
df["latency_ms"] = df["received_at_ms"] - df["timestamp_ms"]

# Compute overall stats
overall_min_latency = df["latency_ms"].min()
overall_median_latency = df["latency_ms"].median()
print(f"Overall minimum latency: {overall_min_latency:.2f} ms")
print(f"Overall median latency: {overall_median_latency:.2f} ms\n")

# Group by relay and compute min latency
min_latency_by_relay = df.groupby("relay")["latency_ms"].min().sort_values()

# Print results
print("Minimum latency (ms) by relay:\n")
for relay, min_latency in min_latency_by_relay.items():
    print(f"{relay}: {min_latency:.2f} ms")

# Plot only min latency as points with different colors
plt.figure(figsize=(10, 8))
y_positions = np.arange(len(min_latency_by_relay))

# Use a colormap to assign different colors
cmap = cm.get_cmap("viridis", len(min_latency_by_relay))
colors = cmap(np.linspace(0, 1, len(min_latency_by_relay)))

plt.scatter(min_latency_by_relay.values, y_positions, color=colors, s=80)

# Add vertical line for overall median latency
plt.axvline(overall_median_latency, color='black', linestyle='--', linewidth=1, label='Overall Median')

# Set axis labels and ticks
plt.yticks(y_positions, min_latency_by_relay.index, fontsize=10)
plt.xlabel("Minimum Latency (ms)", fontsize=12)
plt.title("Minimum Bid Latency by Relay", fontsize=14, fontweight="bold")
plt.grid(axis='x', linestyle='--', linewidth=0.5)
plt.legend()
plt.tight_layout()
plt.show()
