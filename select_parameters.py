import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the CSV
df = pd.read_csv("combined_test_files.csv")  # Replace with actual filename

# Extract agent group from the first letter of winning_agent
df["agent_group"] = df["winning_agent"].str[0]

# Filter for B, S, L only
df = df[df["agent_group"].isin(["B", "S", "L"])]

# Group by agent_group and Reveal, summing cumulative profit
grouped = df.groupby(["agent_group", "Reveal"])["Profit"].sum().reset_index()

# Pivot to get agent_group as rows and Reveal as columns
pivot = grouped.pivot(index="agent_group", columns="Reveal", values="Profit").fillna(0)
pivot = pivot[sorted(pivot.columns)]  # Ensure Reveal values are sorted

# Parameters
agent_groups = pivot.index.tolist()
reveal_values = pivot.columns.tolist()
num_agents = len(agent_groups)
num_reveals = len(reveal_values)
bar_width = 0.1
group_spacing = 0.3

# X positions: leave space between groups
group_width = num_reveals * bar_width
total_width = group_width + group_spacing
x_base = np.arange(num_agents) * total_width

colors = plt.cm.viridis(np.linspace(0, 1, num_reveals))

# Plotting
fig, ax = plt.subplots(figsize=(10, 6))

for i, reveal in enumerate(reveal_values):
    x_pos = x_base + i * bar_width
    ax.bar(x_pos, pivot[reveal], width=bar_width, color=colors[i], label=f"Reveal {reveal}")

# Annotate best Reveal per agent group
for j, agent in enumerate(agent_groups):
    profits = pivot.loc[agent]
    best_reveal = profits.idxmax()
    best_value = profits.max()
    best_index = reveal_values.index(best_reveal)
    x_annotate = x_base[j] + best_index * bar_width
    ax.annotate(
        f"Reveal={best_reveal}",
        xy=(x_annotate, best_value + 0.5),
        ha='center',
        fontsize=9,
        fontweight='bold'
    )

# Axis and formatting
tick_positions = x_base + (num_reveals / 2 - 0.5) * bar_width
ax.set_xticks(tick_positions)
ax.set_xticklabels(agent_groups)
ax.set_xlabel("Strategy of Winning Agent")
ax.set_ylabel("Cumulative Profit")
ax.set_title("Cumulative Profit by Strategy and Time Reveal Epsilon")
ax.legend(title="Reveal", bbox_to_anchor=(1.05, 1), loc="upper left")
ax.grid(axis='y', linestyle='--', alpha=0.5)

plt.tight_layout()
plt.show()
