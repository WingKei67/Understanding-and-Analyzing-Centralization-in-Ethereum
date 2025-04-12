import pandas as pd

# Load the dataset
df = pd.read_csv("total_bids.csv")

# Ensure columns are numeric
df["received_at_ms"] = pd.to_numeric(df["received_at_ms"], errors="coerce")
df["timestamp_ms"] = pd.to_numeric(df["timestamp_ms"], errors="coerce")

# Drop rows with missing values
df = df.dropna(subset=["received_at_ms", "timestamp_ms"])

# Compute the latency
df["latency_ms"] = df["received_at_ms"] - df["timestamp_ms"]

# Compute the mean latency
min_latency = df["latency_ms"].min()
mean_latency = df["latency_ms"].mean()

print()
print(f"Mean latency (received_at_ms - timestamp_ms): {mean_latency:.2f} ms")
