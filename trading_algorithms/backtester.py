from algorithm_class import TradingAlgorithm
from algorithm_factory import algorithm_create, AlgorithmTypes


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
algo = algorithm_create(AlgorithmTypes.MAXIMALLY_GREEDY, starting_balance=100, starting_shares=100)
data = [100, 102.5, 105, 103, 104, 90, 70, 100, 100, 102, 98, 102]
backtest(algo, data)

