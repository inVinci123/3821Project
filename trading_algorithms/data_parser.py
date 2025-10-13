from os.path import join
from datetime import date, datetime


def get_stock_data(stockname: str) -> list[tuple[date, float]]:
    lines: list[tuple[date, float]] = []
    with open(join("data", stockname.lower() + ".csv")) as INPUT:
        for line in INPUT.readlines()[1:]:
            parts = line.split(',')
            found_date = datetime.strptime(parts[0], "%d/%m/%Y").date()
            lines.append((found_date, float(parts[1])))

    return lines


def parse_csv(filename: str) -> list[float]:
    lines: list[float] = []
    with open(join("data", filename)) as INPUT:
        for line in INPUT.readlines()[1:]:
            lines.append(float(line.split(',')[1]))

    return lines

