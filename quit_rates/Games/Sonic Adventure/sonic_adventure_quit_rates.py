import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import PercentFormatter
import numpy as np
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.image as mpimg

# Optional: Load data from Excel
df = pd.read_excel("sonic_adventure_quit_rates.xlsx")

# Set Seaborn style
sns.set_theme(style="whitegrid")
fig, ax = plt.subplots(figsize=(14, 10))

# Format y-axis as percentages
plt.gca().yaxis.set_major_formatter(PercentFormatter(xmax=1, decimals=0))  # xmax=1 assumes y is in 0-1

# List of indexes to highlight (e.g., 5th, 10th, 15th points)
highlight_indexes = [1,5,6]

# Line plot
sns.lineplot(data=df, x='chapter_name', y='quit_rate_pc', marker='o', linewidth=2.5, color='#007acc')
ax.yaxis.set_major_formatter(PercentFormatter(xmax=1))
ax.set_title("Sonic Adventure - Quit Rates", fontsize=18, weight='bold')
ax.set_xlabel("Trophy", fontsize=14)
ax.set_ylabel("Quit Rate", fontsize=14)
plt.xticks(rotation=90)
plt.grid(True, linestyle='--', alpha=0.6)

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

# --- Add PNG image ---
img = mpimg.imread("image.png")
imagebox = OffsetImage(img, zoom=0.6)  # Adjust zoom as needed
ab = AnnotationBbox(imagebox, (1, 1), xycoords='axes fraction', frameon=False,
                    box_alignment=(2.1, 1.1))  # Push it just outside the top right
ax.add_artist(ab)

# Show Plot
plt.tight_layout()
plt.show()