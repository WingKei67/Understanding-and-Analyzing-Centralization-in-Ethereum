import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def load_and_process(path, label):
    df = pd.read_csv(path)
    df['timestamp_ms'] = pd.to_numeric(df['timestamp_ms'], errors='coerce')
    df['value'] = pd.to_numeric(df['value'], errors='coerce') / 1e18  # wei to ETH
    df = df.dropna()
    df = df[df['value'] > 0]
    df = df.sort_values('timestamp_ms')
    df['time_elapsed_sec'] = (df['timestamp_ms'] - df['timestamp_ms'].iloc[0]) / 1000.0
    df['cumulative_value'] = df['value'].cumsum()
    df['source'] = label
    return df[['time_elapsed_sec', 'cumulative_value', 'source']]

# Load real data
real_public = load_and_process('public_transactions.csv', 'Real Public')
real_private = load_and_process('private_transactions.csv', 'Real Private')

# Load simulated data
sim_public = load_and_process('simulated_public_transactions.csv', 'Simulated Public')
sim_private = load_and_process('simulated_private_transactions.csv', 'Simulated Private')

# Plotting
plt.figure(figsize=(12, 6))

# Public
plt.plot(real_public['time_elapsed_sec'], real_public['cumulative_value'],
         label='Real Public', linewidth=2)
plt.plot(sim_public['time_elapsed_sec'], sim_public['cumulative_value'],
         '--', label='Simulated Public')

# Private
plt.plot(real_private['time_elapsed_sec'], real_private['cumulative_value'],
         label='Real Private', linewidth=2)
plt.plot(sim_private['time_elapsed_sec'], sim_private['cumulative_value'],
         '--', label='Simulated Private')

# Labels
plt.title("Cumulative ETH Value Over Time (Simulated vs Real)")
plt.xlabel("Time Elapsed (seconds)")
plt.ylabel("Cumulative ETH")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
