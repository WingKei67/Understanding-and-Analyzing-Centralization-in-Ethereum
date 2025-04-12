import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
df = pd.read_csv("test3.csv")

# Filter rows where last character of winning_agent is '0'
df_filtered = df[df["winning_agent"].str[-1] == '6']

# Extract first letter of winning_agent for grouping
df_filtered["agent_group"] = df_filtered["winning_agent"].str[0]

# Group by first letter and calculate average winning_bid_value
grouped_avg = df_filtered.groupby("agent_group")["Profit"].mean()

# Plot
plt.figure(figsize=(8, 5))
grouped_avg.plot(kind="bar", edgecolor='black')
plt.title("Average Profit by Agent Group (Low, Low, Low)")
plt.xlabel("First Letter of Winning Agent")
plt.ylabel("Average Profit")
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()
