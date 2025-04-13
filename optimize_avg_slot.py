import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
df = pd.read_csv("combined_test_files.csv")

for index in range(8):
    # Filter rows where last character of winning_agent matches index
    df_filtered = df[df["winning_agent"].str[-1] == str(index)].copy()

    # Extract first letter of winning_agent
    df_filtered["agent_group"] = df_filtered["winning_agent"].str[0]

    # Count wins by agent group and normalize
    win_counts = df_filtered["agent_group"].value_counts()
    win_ratios = win_counts / win_counts.sum()

    # Fixed color map for agent groups
    color_map = {
        'N': '#1f77b4',  # blue
        'A': '#ff7f0e',  # orange
        'L': '#2ca02c',  # green
        'S': '#d62728',  # red
        'B': '#9467bd'   # purple
    }

    # Get colors in order of win_ratios index
    bar_colors = [color_map.get(agent, '#7f7f7f') for agent in win_ratios.index]

    # Dimension mapping
    dimension_mapping = {
        0: ('Low', 'Low', 'Low'),
        1: ('High', 'Low', 'Low'),
        2: ('Low', 'High', 'Low'),
        3: ('High', 'High', 'Low'),
        4: ('Low', 'Low', 'High'),
        5: ('High', 'Low', 'High'),
        6: ('Low', 'High', 'High'),
        7: ('High', 'High', 'High')
    }

    # Plot
    plt.figure(figsize=(8, 5))
    bars = plt.bar(win_ratios.index, win_ratios.values, color=bar_colors, edgecolor='black')

    # Add ratio values on top of each bar
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, height,
                 f'{height:.2%}', ha='center', va='bottom', fontsize=10)

    plt.title(f"Win Ratio by Strategy {dimension_mapping[int(index)]}")
    plt.xlabel("Strategy of Winning Player")
    plt.ylabel("Win Ratio")
    plt.ylim(0, 1)
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    plt.tight_layout()

    # Save the figure
    filename = f"plot/win_ratio_by_agent_group_{index}.png"
    plt.savefig(filename)
    plt.close()
