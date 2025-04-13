import pandas as pd
import matplotlib.pyplot as plt
import glob
import numpy as np

# === Load all test*.csv files ===
file_list = glob.glob("test*.csv")
df_all = pd.concat([pd.read_csv(file) for file in file_list], ignore_index=True)

# === Extract agent group (first letter) ===
df_all["agent_group"] = df_all["winning_agent"].str[0]

# === Filter only L, S, B agent groups ===
df_all = df_all[df_all["agent_group"].isin(["L", "S", "B"])]

# === Group and aggregate cumulative profit ===
grouped = df_all.groupby(["agent_group", "time_reveal_epsilon"])["Profit"].sum().reset_index()

# === Pivot table ===
pivot_table = grouped.pivot(index="agent_group", columns="time_reveal_epsilon", values="Profit").fillna(0)
pivot_table = pivot_table[sorted(pivot_table.columns)]

# === Setup for grouped bar plot ===
agent_groups = pivot_table.index.tolist()
epsilons = pivot_table.columns.tolist()
epsilons_index = pd.Index(epsilons)
num_epsilons = len(epsilons)

bar_width = 0.1
group_spacing = 0.3  # Adjusted to reduce gap
group_width = bar_width * num_epsilons
total_width = group_width + group_spacing
x = np.arange(len(agent_groups)) * total_width

colors = plt.cm.viridis(np.linspace(0, 1, num_epsilons))

# === Plot bars ===
plt.figure(figsize=(12, 6))

for i, epsilon in enumerate(epsilons):
    plt.bar(
        x + i * bar_width,
        pivot_table[epsilon],
        width=bar_width,
        label=f"{epsilon}",
        color=colors[i]
    )

# === Annotate top epsilon per group ===
for idx, agent in enumerate(agent_groups):
    profits = pivot_table.loc[agent]
    max_eps = profits.idxmax()
    max_val = profits.max()
    max_pos = x[idx] + epsilons_index.get_loc(max_eps) * bar_width
    plt.annotate(
        f"{max_eps}",
        xy=(max_pos, max_val + 0.2),
        ha='center',
        fontsize=9,
        fontweight='bold'
    )

# === Axis & legend ===
plt.xticks(x + group_width / 2 - bar_width / 2, agent_groups)
plt.xlabel("Strategy of Winning Agent")
plt.ylabel("Cumulative Profit")
plt.title("Cumulative Profit by Strategy and Revealing Time Epsilon")
plt.legend(title="Time Reveal Epsilon", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()
