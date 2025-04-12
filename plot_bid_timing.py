import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import time

# Load your data
df = pd.read_csv("winning_bids_labeled.csv")

# Column names
timestamp_col = 'date'
slot_time_ms_col = 'slot_t_ms'
value_col = 'value'
builder_col = 'builder_label'

# Convert timestamp and extract date string
df[timestamp_col] = pd.to_datetime(df[timestamp_col], errors='coerce')  # Robust parsing
df['date_str'] = df[timestamp_col].dt.strftime('%Y-%m-%d')

# Check available dates
print("Available dates in the data:")
print(df['date_str'].value_counts().sort_index())

# === Change this to the target date ===
target_date = '2025-03-01'

# Filter for the target date
df_day = df[df['date_str'] == target_date].copy()

# Convert units
df_day['slot_time_sec'] = df_day[slot_time_ms_col] / 1000
df_day['value_eth'] = df_day[value_col] / 1e18

# Plot
plt.figure(figsize=(12, 8))
sns.scatterplot(
    data=df_day,
    x='slot_time_sec',
    y='value_eth',
    hue=builder_col,
    palette='tab20',
    edgecolor=None,
    alpha=0.6,
    s=25
)

# Compute and plot Q1, median, Q3 (horizontal lines for global reference)
q1 = df_day['value_eth'].quantile(0.25)
median = df_day['value_eth'].median()
q3 = df_day['value_eth'].quantile(0.75)

plt.axhline(q1, color='gray', linestyle='--', linewidth=1, alpha=0.6, label='Q1 (25%)')
plt.axhline(median, color='black', linestyle='-', linewidth=1.2, alpha=0.8, label='Median (50%)')
plt.axhline(q3, color='gray', linestyle='--', linewidth=1, alpha=0.6, label='Q3 (75%)')

# Labels and legend
plt.xlabel("Seconds in slot")
plt.ylabel("ETH")
plt.title(f"Timing of Successful Bids ({target_date})")
plt.grid(True)

# Place legend
plt.legend(
    title="Builder",
    loc='center left',
    bbox_to_anchor=(1.01, 0.5),
    borderaxespad=0,
    frameon=True
)

plt.tight_layout()
plt.show()
