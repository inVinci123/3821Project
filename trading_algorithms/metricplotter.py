# Code modified from example at
# https://matplotlib.org/stable/gallery/lines_bars_and_markers/barchart.html

import matplotlib.pyplot as plt
import numpy as np
from math import floor, ceil

algorithms = ("Greedy", "Random", "Best after 10",)# "SMA", "EMA", "BOLLINGER (1STD)")
graphables = {
    'Overall Multiplier': (0.916582, 1.70491, 1.15507),
    'Yearly Sharpe Ratio': (-0.0844388, 0.310548, 0.0285646),
    'Calmar Ratio': (-0.0273064, 0.101462, 0.0285646),
    'Average Trade': (-1.0739471, 0.691274, 12.9725)
}

highest = 0
lowest = 0

# Round values to 2dp and get graph y-bounds
for key in graphables:
    graphables[key] = tuple(round(num, 2) for num in graphables[key])
    lowest = min(lowest, min(graphables[key]))
    highest = max(highest, max(graphables[key]))

x = np.arange(len(algorithms))  # the label locations
width = 0.1  # the width of the bars
multiplier = 0

fig, ax = plt.subplots(layout='constrained')

for attribute, measurement in graphables.items():
    offset = width * multiplier
    rects = ax.bar(x + offset, measurement, width, label=attribute)
    ax.bar_label(rects, padding=1)
    multiplier += 1

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Value')
ax.set_title('Metrics of algorithms in bullish stocks')
ax.set_xticks(x + width * 1.5, algorithms)
ax.legend(loc='upper left', ncols=4)
ax.set_ylim(floor(lowest), ceil(highest))

plt.show()
