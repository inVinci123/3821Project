# Code modified from example at
# https://matplotlib.org/stable/gallery/lines_bars_and_markers/barchart.html

import matplotlib.pyplot as plt
import numpy as np
from math import floor, ceil

# algorithms = ("Greedy", "Random", "Best after 10", "SMA", "EMA", "BOLLINGER (1STD)", "BOLLINGER (2STD)", "RSI")#, "PPO ML")
algorithms = ("Greedy", "Greedy (following)", "Random", "Best after 10", "SMA", "EMA", "BOLLINGER (1STD)", "BOLLINGER (2STD)", "RSI")#, "PPO ML")
graphables = {
    ## Bullish
    ## 'Overall Multiplier': (0.877759,1.67967,1.13533,1.81938,1.75907,1.39696,1.48725,1.248),#3,47.8379),
    ## 'Yearly Sharpe Ratio': (-0.14618,0.782871,0.304294,0.577865,0.555752,0.547657,0.669194,0.572905),#,0.155094),
    ## 'Calmar Ratio': (-0.03584,0.103638,0.021931,0.10845,0.10487,0.060160,0.077169,0.064379),#,0.2521),
    ## 'Average Trade': (-0.10500,0.722603,7.78982,13.1893,39.2725,0.553747,3.3242,35.6848,31997.1)

    ## Sideways
    ## 'Overall Multiplier': (0.81186,1.06121,0.99742,0.99697,0.87749,1.21159,1.30656,1.0956,9.57492),
    ## 'Yearly Sharpe Ratio': (-0.4381,0.08543,0.07515,0.03048,-0.1358,0.22485,0.49475,0.32438,0.22962),
    ## 'Calmar Ratio': (-0.0501,0.00885,-0.0019,-0.0033,-0.0253,0.03131,0.05413,0.01761,0.14305),
    ##'Average Trade': (-0.1455,0.06273,0.58621,0.27043,-4.6860,0.34116,2.06816,18.2502,4696.42)

    ## Bearish
    ## 'Overall Multiplier': (0.49568,0.73214,0.61581,0.85085,0.81089,0.64810,0.66961,0.71637),#17.4977),
    ## 'Yearly Sharpe Ratio': (-1.1725,-0.4949,-0.4776,-0.2601,-0.3519,-0.5161,-0.4794,-0.3234),#0.44419),
    ## 'Calmar Ratio': (-0.1520,-0.0638,-0.1121,-0.0347,-0.0343,-0.1024,-0.0956,-0.0665)#,0.42232),
    ## 'Average Trade': (-0.4010,-0.2599,-259.66,-1.5074,-3.4613,-0.5761,-2.3954,-24.211,3521.99)


    # Bullish
    'Overall Multiplier': (0.87775,5.38435,1.59433,1.13533,1.81938,1.75907,1.39696,1.48725,1.2483),
    'Yearly Sharpe Ratio': (-0.1461,1.46712,0.73600,0.30429,0.57786,0.55575,0.54765,0.66919,0.57290),
    'Calmar Ratio': (-0.0358,0.23641,0.09210,0.02193,0.10845,0.10487,0.06016,0.07716,0.06437),
    # 'Average Trade': (-0.1050,2.94284,0.62126,7.78982,13.1893,39.2725,0.55374,3.3242,35.6848)

    # Sideways
    # 'Overall Multiplier': (0.81186,1.6077,1.14239,0.99742,0.99697,0.87749,1.21159,1.30656,1.0956),
    # 'Yearly Sharpe Ratio': (-0.4381,0.72709,0.20230,0.07515,0.03048,-0.1358,0.22485,0.49475,0.32438),
    # 'Calmar Ratio': (-0.0501,0.08642,0.02243,-0.0019,-0.0033,-0.0253,0.03131,0.05413,0.01761),
    # 'Average Trade': (-0.1455,0.48579,0.14619,0.58621,0.27043,-4.6860,0.34116,2.06816,18.2502)

    # Bearish
    # 'Overall Multiplier': (0.49568,1.39084,0.75201,0.61581,0.85085,0.81089,0.64810,0.66961,0.71637),
    # 'Yearly Sharpe Ratio': (-1.1725,0.30648,-0.4679,-0.4776,-0.2601,-0.3519,-0.5161,-0.4794,-0.3234),
    # 'Calmar Ratio': (-0.1520,0.04100,-0.0607,-0.1121,-0.0347,-0.0343,-0.1024,-0.0956,-0.0665),
    # 'Average Trade': (-0.4010,0.27015,-0.2578,-259.66,-1.5074,-3.4613,-0.5761,-2.3954,-24.211)
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
ax.set_title('Average metrics of algorithms in bearish stocks')
ax.set_xticks(x + width, algorithms)
ax.legend(loc='lower left', ncols=4)
ax.set_ylim(lowest - 0.1, highest + 0.1)

plt.show()
