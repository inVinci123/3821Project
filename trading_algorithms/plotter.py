import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, DayLocator, WeekdayLocator
from sys import argv
from data_parser import get_stock_data


if len(argv) <= 1:
    exit(-1)

stockname = argv[1].strip()
stock = get_stock_data(stockname)
dates = [p[0] for p in stock]
values = [p[1] for p in stock]
date_ticks = []
for date in dates:
    month_days = (d.day for d in dates if (d.month, d.year) == (date.month, date.year) and d.day >= dates[-1].day)
    if date.day == min(month_days):
        date_ticks.append(date)
        continue
date_ticks.append(dates[0])

date_labels = [date.strftime("%d/%m/%Y") for date in date_ticks]

plt.gca().xaxis.set_major_formatter(DateFormatter("%d/%m/%Y"))
plt.gca().xaxis.set_major_locator(DayLocator(bymonthday=dates[0].day))
plt.xlim(dates[0], dates[-1])

plt.plot(dates, values)
plt.xticks(date_ticks, date_labels)
plt.gcf().autofmt_xdate()

plt.xlabel("Date")
plt.ylabel("Value")
plt.title("Stock")
plt.grid(True)

import matplot2tikz
print(matplot2tikz.get_tikz_code())
plt.show()
# plt.savefig("images/" + stockname + ".png")

