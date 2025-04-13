import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load CSV
df = pd.read_csv("combined_test_files.csv")

# Group by agent and sum profits
profit_sums = df.groupby("winning_agent")["Profit"].sum().sort_values(ascending=False)

# Top 10 agents + Others
top_profits = profit_sums.head(10)
others = profit_sums.iloc[10:].sum()
if others > 0:
    top_profits["Others"] = others

# Common accessible colors
colors = [
    '#4e79a7', '#f28e2b', '#e15759', '#76b7b2', '#59a14f',
    '#edc948', '#b07aa1', '#ff9da7', '#9c755f', '#bab0ab', '#cccccc'
]

# Explode effect
explode = [0.1 if i == 0 else 0.05 for i in range(len(top_profits))]

# Plot
fig, ax = plt.subplots(figsize=(12, 10))
wedges, _ = ax.pie(
    top_profits,
    labels=[''] * len(top_profits),
    startangle=140,
    colors=colors[:len(top_profits)],
    explode=explode,
    wedgeprops=dict(width=0.4)
)

# Add labels for agents with >3% profit share
total = top_profits.sum()
for i, (wedge, agent, value) in enumerate(zip(wedges, top_profits.index, top_profits.values)):
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
print("Cumulative Profit Share by Top Winning Players:\n")
for agent, value in top_profits.items():
    pct = value / total
    print(f"{agent}: {pct:.2%}")


# Title with spacing
ax.set_title("Cumulative Profit Share by Top Winning Players", fontsize=16, pad=30)
ax.axis('equal')
plt.tight_layout()
plt.savefig("plot/cumulative_profit_share_pie_clean.png")
plt.show()
plt.close()