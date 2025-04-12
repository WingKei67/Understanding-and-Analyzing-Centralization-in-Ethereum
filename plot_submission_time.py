import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

# Load the dataset
df = pd.read_csv("winning_bids_labeled.csv")

# Group by builder label
grouped = df.groupby("builder_label")["slot_t_ms"]

# Prepare data for boxplot
builder_labels = []
delay_data = []

for label, delays in grouped:
    builder_labels.append(label)
    delay_data.append(delays)

# Define color palette
cmap = cm.get_cmap("tab20b", len(delay_data))

# Plot
fig, ax = plt.subplots(figsize=(8, 9))
box = ax.boxplot(
    delay_data,
    vert=False,
    patch_artist=True,
    showfliers=False,
    widths=0.6,
    medianprops=dict(color='black', linewidth=2),
    whiskerprops=dict(color='gray', linewidth=1.5),
    capprops=dict(color='gray', linewidth=1.5),
    boxprops=dict(linewidth=1.5)
)

# Color each box uniquely
for patch, color in zip(box["boxes"], cmap(np.linspace(0, 1, len(delay_data)))):
    patch.set_facecolor(color)

# Add vertical line at t=0 (start of slot)
ax.axvline(0, color="black", linestyle="--", linewidth=1)

# Axis labels & ticks
ax.set_yticks(range(1, len(builder_labels) + 1))
ax.set_yticklabels(builder_labels, fontsize=10)
ax.set_xlabel("Time (ms)", fontsize=12)
ax.set_ylabel("Builders", fontsize=12)
ax.set_title("Winning bids submission time", fontsize=14, fontweight="bold")

# Grid and layout
ax.grid(axis="x", linestyle="--", linewidth=0.5)
plt.tight_layout()
plt.show()
