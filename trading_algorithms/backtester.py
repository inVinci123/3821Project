from algorithm_class import TradingAlgorithm
from algorithm_factory import algorithm_create, AlgorithmTypes
from data_parser import parse_csv


def backtest(algorithm: TradingAlgorithm, data: list[float], print_results: bool = True):
    """
    Run a back test on a given algorithm with given data points
    """
    for datum in data:
        algorithm.give_data_point(datum)
        if print_results:
            print(
                f"=== {algorithm.get_current_index():5} ===\n"
                f"Balance: {algorithm.get_current_balance():.03f}\n"
                f"Shares:  {algorithm.get_current_shares():.03f}   (at {datum} each)\n"
                f"Total worth: {algorithm.get_current_worth(datum):.03f}")


# Simple test case
# data = [100, 102.5, 105, 103, 104, 90, 70, 100, 100, 102, 98, 102]
# print("GREEDY")
# gred = algorithm_create(AlgorithmTypes.MAXIMALLY_GREEDY, starting_balance=100, starting_shares=100)
# backtest(gred, data)
#
# print("\n\n\nRANDOM\n\n\n")
#
# rand = algorithm_create(AlgorithmTypes.RANDOM_CHOICE, starting_balance=100, starting_shares=100)
# backtest(rand, data)

# Standardising testing
data = parse_csv("nabax.csv")

start_balance = 100
start_shares = 50
start_value = round(start_balance + start_shares * data[0], 3)

print("GREEDY")

greedy_long = algorithm_create(AlgorithmTypes.MAXIMALLY_GREEDY, start_balance, start_shares)
random_long = algorithm_create(AlgorithmTypes.RANDOM_CHOICE, start_balance, start_shares)

backtest(greedy_long, data, False)
print(         
    f"Balance: {start_balance} -> {greedy_long.get_current_balance():.03f}\n"
        f"Shares:  {start_balance} -> {greedy_long.get_current_shares():.03f}   (at {data[-1]:.03f} each)\n"
    f"TWorth:  {start_value} -> {greedy_long.get_current_worth(data[-1]):.03f}")

print("\nRANDOM")

backtest(random_long, data, False)
print(         
    f"Balance: {start_balance} -> {random_long.get_current_balance():.03f}\n"
        f"Shares:  {start_balance} -> {random_long.get_current_shares():.03f}   (at {data[-1]:.03f} each)\n"
    f"TWorth:  {start_value} -> {random_long.get_current_worth(data[-1]):.03f}")

