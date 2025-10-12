import matplotlib.pyplot as plt
from sys import stdin, argv

if len(argv) > 1:
    with open(argv[1]) as INPUT:
        input = INPUT.read()
else:
    input = stdin.read()

# Read lines after CSV header
textin = input.strip().split('\n')[1:]
if ',' in textin[0]:
    # Commas in data mean actual Date,Value CSV data was passed in
    textin = [line.split(',')[1] for line in textin]

# Convert to numbers
values = [float(x) for x in textin]

plt.plot(values)
plt.ylabel("Value")
plt.title("Stock")
plt.grid(True)

import matplot2tikz
print(matplot2tikz.get_tikz_code())
plt.show()

