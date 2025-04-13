import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load CSV
df = pd.read_csv("combined_test_files.csv")

# Group by winning_agent
total_profit = df.groupby("winning_agent")["Profit"].sum()
win_count = df["winning_agent"].value_counts()
avg_profit = (total_profit / win_count).sort_values(ascending=False)

# Top 10 + Others
top_avg = avg_profit.head(10)
others_avg = avg_profit.iloc[10:].mean()  # take mean of the rest
if len(avg_profit) > 10:
    top_avg["Others"] = others_avg

# Common color palette
colors = [
    '#4e79a7', '#f28e2b', '#e15759', '#76b7b2', '#59a14f',
    '#edc948', '#b07aa1', '#ff9da7', '#9c755f', '#bab0ab', '#cccccc'
]

# Explode effect
explode = [0.1 if i == 0 else 0.05 for i in range(len(top_avg))]

# Plot
fig, ax = plt.subplots(figsize=(12, 10))
wedges, _ = ax.pie(
    top_avg,
    labels=[''] * len(top_avg),
    startangle=140,
    colors=colors[:len(top_avg)],
    explode=explode,
    wedgeprops=dict(width=0.4)
)

# Filter out small shares
total = top_avg.sum()
for i, (wedge, agent, value) in enumerate(zip(wedges, top_avg.index, top_avg.values)):
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
ax.set_title("Average Profit per Win by Top Winning Players", fontsize=16, pad=30)
ax.axis('equal')
plt.tight_layout()
plt.savefig("plot/avg_profit_per_win_pie_clean.png")
plt.show()
plt.close()
