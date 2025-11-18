# Code modified from example at
# https://matplotlib.org/stable/gallery/lines_bars_and_markers/barchart.html

import matplotlib.pyplot as plt
import numpy as np
from math import floor, ceil

algorithms = ("Greedy", "Random", "Best after 10", "SMA", "EMA", "BOLLINGER (1STD)", "BOLLINGER (2STD)", "RSI", "PPO ML")
graphables = {
    'Overall Multiplier' : (0.877759,1.67967,1.13533,1.81938,1.75907,1.39696,1.48725,1.2483,47.8379),
    'Yearly Sharpe Ratio' : (-0.14618,0.782871,0.304294,0.577865,0.555752,0.547657,0.669194,0.572905,0.155094),
    'Calmar Ratio' : (-0.03584,0.103638,0.021931,0.10845,0.10487,0.060160,0.077169,0.064379,0.2521),
    # 'Average Trade' : (-0.10500,0.722603,7.78982,13.1893,39.2725,0.553747,3.3242,35.6848,31997.1)
}

highest = 0
lowest = 0

# Round values to 2dp and get graph y-bounds
for key in graphables:
    graphables[key] = tuple(round(num, 2) for num in graphables[key])
    lowest = min(lowest, min(graphables[key]))
    highest = max(highest, max(graphables[key]))

x = np.arange(len(algorithms))  # the label locations
width = 0.2  # the width of the bars
multiplier = 0

fig, ax = plt.subplots(layout='constrained')

for attribute, measurement in graphables.items():
    offset = width * multiplier
    rects = ax.bar(x + offset, measurement, width, label=attribute)
    ax.bar_label(rects, padding=1)
    multiplier += 1

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_xlabel('Algorithms')
ax.set_ylabel('Value')
ax.set_title('Average metrics of algorithms in bullish stocks')
ax.set_xticks(x + width * 1.5, algorithms)
ax.legend(loc='upper left', ncols=3)
ax.set_ylim(lowest - 0.1, ceil(highest) + 0.3)

plt.show()
