import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import PercentFormatter
import numpy as np

# Optional: Load data from Excel
df = pd.read_excel("mafia_2_de_quit_rates.xlsx")

# Set Seaborn style
sns.set_theme(style="whitegrid")

# Create the plot
plt.figure(figsize=(14, 10))
sns.lineplot(data=df, x='chapter_name', y='quit_rate_pc', marker='o', linewidth=2.5, color='#007acc')

# Format y-axis as percentages
plt.gca().yaxis.set_major_formatter(PercentFormatter(xmax=1, decimals=0))  # xmax=1 assumes y is in 0-1

# List of indexes to highlight (e.g., 5th, 10th, 15th points)
highlight_indexes = [1, 13, 14]

# Highlight selected points
for idx in highlight_indexes:
    point = df.iloc[idx]
    plt.plot(
        point['chapter_name'],
        point['quit_rate_pc'],
        'o',
        markersize=12,
        markerfacecolor='none',
        markeredgecolor='red',
        markeredgewidth=2
    )
    plt.annotate(
        f"{point['quit_rate_pc']:.1%}",
        xy=(point['chapter_name'], point['quit_rate_pc']),
        xytext=(10, 10),
        textcoords='offset points',
        arrowprops=dict(arrowstyle='->', color='red'),
        fontsize=10,
        color='red'
    )

# Enhance aesthetics
plt.title("Mafia 2: Definitive Edition - Quit Rates", fontsize=18, weight='bold', color='#333333')
plt.xlabel("Chapter Name", fontsize=14)
plt.ylabel("Quit Rate", fontsize=14)
plt.xticks(rotation=90)
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()
