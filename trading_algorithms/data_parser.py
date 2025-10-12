from os.path import join


def parse_csv(filename: str) -> list[float]:
    lines: list[float] = []
    with open(join("data", filename)) as INPUT:
        for line in INPUT.readlines()[1:]:
            lines.append(float(line.split(',')[1]))

    return lines

