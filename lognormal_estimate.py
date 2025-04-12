import pandas as pd
import numpy as np
from scipy.stats import lognorm

# === Load dataset ===
df = pd.read_csv("processed/block_transaction_summary2.csv")

# === Convert value from wei to ETH ===
df["value"] = df["value"].astype(float) / 1e18

# === Split value into public and private+unknown parts ===
df["public_value"] = 0.3 * df["value"]
df["private_unknown_value"] = 0.7 * df["value"]

# === Compute tx group counts ===
df["public_tx_count"] = pd.to_numeric(df["public_tx_count"], errors="coerce")
df["private_unknown_tx_count"] = (
    pd.to_numeric(df["private_tx_count"], errors="coerce") +
    pd.to_numeric(df["unknown_tx_count"], errors="coerce")
)

# === Filter valid rows ===
df = df[
    (df["public_value"] > 0) &
    (df["private_unknown_value"] > 0) &
    (df["public_tx_count"] > 0) &
    (df["private_unknown_tx_count"] > 0)
]

# === Compute per-tx value ===
df["value_per_public_tx"] = df["public_value"] / df["public_tx_count"]
df["value_per_private_unknown_tx"] = df["private_unknown_value"] / df["private_unknown_tx_count"]

# === Expand the data to weight each per-tx value by its count ===
public_values_expanded = np.repeat(df["value_per_public_tx"].values, df["public_tx_count"].astype(int).values)
private_values_expanded = np.repeat(df["value_per_private_unknown_tx"].values, df["private_unknown_tx_count"].astype(int).values)

# === Fit lognormal distributions ===
shape_pub, loc_pub, scale_pub = lognorm.fit(public_values_expanded, floc=0)
mu_pub = np.log(scale_pub)
sigma_pub = shape_pub

shape_priv, loc_priv, scale_priv = lognorm.fit(private_values_expanded, floc=0)
mu_priv = np.log(scale_priv)
sigma_priv = shape_priv

# === Print results ===
print("Estimated Lognormal Distribution for public tx value (weighted):")
print(f"  μ (mean of log): {mu_pub:.4f}")
print(f"  σ (std of log):  {sigma_pub:.4f}")
print(f"  E[value_per_public_tx]: {np.exp(mu_pub + 0.5 * sigma_pub**2):.6f} ETH")

print()

print("Estimated Lognormal Distribution for private+unknown tx value (weighted):")
print(f"  μ (mean of log): {mu_priv:.4f}")
print(f"  σ (std of log):  {sigma_priv:.4f}")
print(f"  E[value_per_private_unknown_tx]: {np.exp(mu_priv + 0.5 * sigma_priv**2):.6f} ETH")

print(np.exp(mu_pub + 0.5 * sigma_pub**2) * df["public_tx_count"].mean() + np.exp(mu_priv + 0.5 * sigma_priv**2) * df["private_unknown_tx_count"].mean())