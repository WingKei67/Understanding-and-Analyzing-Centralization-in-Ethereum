import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import lognorm

# Load the dataset
df = pd.read_csv("total_bids.csv")

# Ensure timestamp_ms is numeric
df["timestamp_ms"] = pd.to_numeric(df["timestamp_ms"], errors="coerce")

# Drop rows with missing data
df = df.dropna(subset=["builder_pubkey", "slot", "timestamp_ms"])

# Sort by builder and slot, then timestamp
df = df.sort_values(by=["builder_pubkey", "slot", "timestamp_ms"])

# Group by builder_pubkey and slot, calculate time differences
df["timestamp_diff"] = df.groupby(["builder_pubkey", "slot"])["timestamp_ms"].diff()

# Drop NaNs (first row in each group has NaN diff)
df_cleaned = df.dropna(subset=["timestamp_diff"])

# Keep only positive values for lognormal fitting
data = df_cleaned["timestamp_diff"]
data = data[data > 0]

# Fit a lognormal distribution
shape, loc, scale = lognorm.fit(data, floc=0)  # Fix location at 0 for true lognormal
mu = np.log(scale)
sigma = shape

print(f"Estimated log-normal parameters:")
print(f"  μ (mean of log): {mu:.4f}")
print(f"  σ (std of log):  {sigma:.4f}")

# Plot histogram and fitted PDF
plt.figure(figsize=(10, 6))
count, bins, ignored = plt.hist(data, bins=100, density=True, color="skyblue", edgecolor="black", alpha=0.6, label="Data Histogram")

# Plot fitted PDF
x = np.linspace(0, data.max(), 1000)
pdf = lognorm.pdf(x, shape, loc=0, scale=scale)
plt.plot(x, pdf, 'r-', linewidth=2, label=f'Log-normal Fit\nμ={mu:.2f}, σ={sigma:.2f}')

# Mean line
mean_diff = data.mean()
plt.axvline(mean_diff, color="black", linestyle="--", linewidth=1.5, label=f"Mean = {mean_diff:.2f} ms")

plt.title("Log-normal Fit: Timestamp Differences Between Adjacent Bids", fontsize=14, fontweight="bold")
plt.xlabel("Timestamp Difference (ms)", fontsize=12)
plt.ylabel("Density", fontsize=12)
plt.legend()
plt.grid(True, linestyle="--", linewidth=0.5)
plt.tight_layout()
plt.show()
