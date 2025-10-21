def get_optimal_worth_history(data: list[float], starting_balance: float, starting_shares: float) -> list[float]:
    """
    Find the truly optimal amount of money that could be made...
    at the cost of breaking causality
    """
    bal = starting_balance
    shares = starting_shares
    worth_history: list[float] = [bal + shares * data[0]]

    for i in range(len(data) - 1):
        if data[i] < data[i + 1]:
            # Will increase: buy
            shares += bal / data[i]
            bal = 0
        elif data[i] > data[i + 1]:
            # Will decrease: sell
            bal += shares * data[i]
            shares = 0

        worth_history.append(bal + shares * data[i])

    # At the last data point, buying and selling doesn't matter
    worth_history.append(bal + shares * data[-1])
    return worth_history

