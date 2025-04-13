import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load CSV
df = pd.read_csv("combined_test_files.csv")

# Count wins
win_counts = df["winning_agent"].value_counts().sort_values(ascending=False)

# Top 10 agents + Others
top_agents = win_counts.head(10)
others = win_counts.iloc[10:].sum()
if others > 0:
    top_agents["Others"] = others

# Use more common, accessible colors
colors = [
    '#4e79a7', '#f28e2b', '#e15759', '#76b7b2', '#59a14f',
    '#edc948', '#b07aa1', '#ff9da7', '#9c755f', '#bab0ab', '#cccccc'
]

# Explode effect
explode = [0.1 if i == 0 else 0.05 for i in range(len(top_agents))]

# Plot
fig, ax = plt.subplots(figsize=(12, 10))
wedges, _ = ax.pie(
    top_agents,
    labels=[''] * len(top_agents),
    startangle=140,
    colors=colors[:len(top_agents)],
    explode=explode,
    wedgeprops=dict(width=0.4)
)

# Add labels for agents with >3%
total = top_agents.sum()
for i, (wedge, agent, value) in enumerate(zip(wedges, top_agents.index, top_agents.values)):
    pct = value / total
    if pct < 0.03:
        continue

    angle = (wedge.theta2 + wedge.theta1) / 2
    angle_rad = np.deg2rad(angle)
    x = 1.1 * np.cos(angle_rad)
    y = 1.1 * np.sin(angle_rad)
    ha = 'left' if x > 0 else 'right'
    label = f"{agent}: {pct:.1%}"

    ax.text(x, y, label, ha=ha, va='center', fontsize=12,
            bbox=dict(fc='white', ec='none', pad=1.5))

# Title with spacing
ax.set_title("Auction Wins by Top Winning Players", fontsize=16, pad=30)
ax.axis('equal')
plt.tight_layout()
plt.savefig("plot/winning_share_pie_clean.png")
plt.show()
plt.close()
