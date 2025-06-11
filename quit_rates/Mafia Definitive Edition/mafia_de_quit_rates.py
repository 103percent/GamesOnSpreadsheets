import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import PercentFormatter
import numpy as np

# Optional: Load data from Excel
df = pd.read_excel("mafia_de_quit_rates.xlsx")

# Set Seaborn style
sns.set_theme(style="whitegrid")

# Create the plot
plt.figure(figsize=(14, 10))
sns.lineplot(data=df, x='chapter_name', y='quit_rate_pc', marker='o', linewidth=2.5, color='#007acc')

# Format y-axis as percentages
plt.gca().yaxis.set_major_formatter(PercentFormatter(xmax=1, decimals=0))  # xmax=1 assumes y is in 0-1

# Identify the point to highlight
highlight_point = df.iloc[4]

# Highlight specific point
plt.plot(
    highlight_point['chapter_name'],
    highlight_point['quit_rate_pc'],
    'o',
    markersize=12,
    markerfacecolor='none',
    markeredgecolor='red',
    markeredgewidth=2,
    label='Pinch Point'
)

# Optional annotation
plt.annotate(
    f"{highlight_point['quit_rate_pc']:.1%}",
    xy=(highlight_point['chapter_name'], highlight_point['quit_rate_pc']),
    xytext=(10, 10),
    textcoords='offset points',
    arrowprops=dict(arrowstyle='->', color='red'),
    fontsize=12,
    color='red'
)

# Enhance aesthetics
plt.title("Mafia: Definitive Edition - Quit Rates", fontsize=18, weight='bold', color='#333333')
plt.xlabel("Chapter Number", fontsize=14)
plt.ylabel("Quit Rate", fontsize=14)
plt.xticks(rotation=90)
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()
