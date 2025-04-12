import pandas as pd

# Load the CSV file
df = pd.read_csv("processed/block_transaction_summary.csv")

# Convert columns to numeric
df["public_tx_count"] = pd.to_numeric(df["public_tx_count"], errors='coerce')
df["private_tx_count"] = pd.to_numeric(df["private_tx_count"], errors='coerce')
df["unknown_tx_count"] = pd.to_numeric(df["unknown_tx_count"], errors='coerce')

# Calculate total and ratio
df["total_tx_count"] = df["public_tx_count"] + df["private_tx_count"] + df["unknown_tx_count"]
df["private_unknown_ratio"] = (df["private_tx_count"] + df["unknown_tx_count"]) / df["total_tx_count"]

# Drop NaN values
df = df.dropna(subset=["private_unknown_ratio", "builder_pubkey"])

# Identify top 10 builders by number of blocks
top_builders = df["builder_pubkey"].value_counts().nlargest(8).index

# Filter for top builders
df_top = df[df["builder_pubkey"].isin(top_builders)]

# Filter ratio range
df_top = df_top[(df_top["private_unknown_ratio"] > 0.10) & (df_top["private_unknown_ratio"] < 0.50)]

# Group and compute stats
grouped_stats = df_top.groupby("builder_pubkey")["private_unknown_ratio"].agg(["min", "mean", "max"]).reset_index()

# Save results
grouped_stats.to_csv("processed/private_unknown_ratio_top10_builders.csv", index=False)

# Display
print(grouped_stats)
