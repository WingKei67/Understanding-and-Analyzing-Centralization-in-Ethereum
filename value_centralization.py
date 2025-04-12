import pandas as pd

# Load data
df = pd.read_csv("winning_bids_labeled.csv")

# Convert from gwei to ETH
df["value_eth"] = df["value"] / 1e9

# Group by builder label and sum profits
profit_by_builder = df.groupby("label")["value_eth"].sum().sort_values(ascending=False)

# Total profit
total_profit = profit_by_builder.sum()

# Cumulative share
profit_by_builder_cumsum = profit_by_builder.cumsum()
profit_by_builder_percent = profit_by_builder_cumsum / total_profit * 100

# Construct table: for k = 1 to N
epsilon_table = pd.DataFrame({
    "Top_k_builders": range(1, len(profit_by_builder) + 1),
    "Cumulative_Profit_Percent": profit_by_builder_percent.values
})

# Save to CSV or display
epsilon_table.to_csv("epsilon_centralization.csv", index=False)
print(epsilon_table.head(20))  # show first 20 entries
