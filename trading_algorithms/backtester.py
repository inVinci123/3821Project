import matplotlib.pyplot as plt
import mpl_axes_aligner as mpl
from algorithm_class import TradingAlgorithm
from algorithm_factory import algorithm_create, AlgorithmTypes
from data_parser import parse_csv
from algorithms.true_optimal import get_optimal_worth_history
from typing import cast
from algorithms.simple_moving_average import SimpleMAAlgorithm
from algorithms.expo_moving_average import ExponentialMAAlgorithm
from algorithms.bollinger import BollingerBandsAlgorithm


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
# testing_stocks = ["MSFT", "AAPL", "NVDA", "NAB.AX", "BTC-USD", "CBA.AX", "ANZ.AX"]
# testing_stocks = ["dowjonesmonthly100y", "ASX.AX"]

# stocks to run data on
testing_stocks = ["BTC-USD"]
for stock in testing_stocks:
    data = parse_csv(stock.lower() + ".csv")
    # data = data * 10
    start_balance = 1000
    start_shares = 0
    true_optimal = get_optimal_worth_history(data, start_balance, start_shares)
    start_value = round(start_balance + start_shares * data[0], 3)

    fig, stockAxes = plt.subplots()
    plt.title(stock)
    plt.xlabel("Days since start")
    stockAxes.set_ylabel("Stock Value")
    stockAxes.plot(data, 'k-+')
    stockAxes.set_xlim(0, len(data) - 1)

    print(f"\n=== {stock} ===")

    greedy_long = algorithm_create(AlgorithmTypes.MAXIMALLY_GREEDY, start_balance, start_shares)
    random_long = algorithm_create(AlgorithmTypes.RANDOM_CHOICE, start_balance, start_shares, [0.3, (0.4, 0.4)])
    best_after_long = algorithm_create(AlgorithmTypes.BEST_AFTER_N, start_balance, start_shares)
    expo_ma_long = cast(ExponentialMAAlgorithm, algorithm_create(AlgorithmTypes.EXPONENTIAL_MA, start_balance, start_shares, [1.0, (5, 21)]))
    expo_ma_long2 = algorithm_create(AlgorithmTypes.EXPONENTIAL_MA, start_balance, start_shares)
    simple_ma_long = cast(SimpleMAAlgorithm, algorithm_create(AlgorithmTypes.SIMPLE_MA, start_balance, start_shares, [1.0, (5, 21)]))
    simple_ma_long2 = algorithm_create(AlgorithmTypes.SIMPLE_MA, start_balance, start_shares)
    bb_1std = BollingerBandsAlgorithm(start_balance, start_shares, num_std_dev=1.0)
    bb_2std = BollingerBandsAlgorithm(start_balance, start_shares, num_std_dev=2.0)

    algoAxes = stockAxes.twinx()
    algoAxes.set_ylabel("Worth history")

    def run_backtest(algorithm, name):
        print(name)

        backtest(algorithm, data, False)
        print(
            f"Balance: {start_balance} -> {algorithm.get_current_balance():.03f}\n"
            f"Shares:  {start_balance} -> {algorithm.get_current_shares():.03f}   (at {data[-1]:.03f} each)\n"
            f"TWorth:  {start_value} ({data[0]:.03f}) -> {algorithm.get_current_worth(data[-1]):.03f}\n")

    algs = [
        # (random_long, "RANDOM", "r--"),
        # (expo_ma_long, "EXPO MA (5, 21)", "b--"),
        (simple_ma_long, "SIMPLE MA (5, 21)", "y--"),
        (bb_1std, "BOLLINGER 1STD", "g--"),
        # (bb_2std, "BOLLINGER 2STD", "m--"),
        # (greedy_long, "Greedy", "c--")
    ]

    for alg in algs:
        run_backtest(*alg[:2])
        final_point = alg[0].get_current_worth(data[-1])
        final_data = alg[0].get_worth_history() + [final_point]
        algoAxes.plot(final_data, alg[2], label=alg[1])

    stockAxes_legend = ["Stock Value"]

    # ---------------------- PLOTTING INDICATORS ----------------------
    
    # for length, history in simple_ma_long.ma_histories.items():
    #     stockAxes.plot(history, label=f"SMA ({length})")
    for length, history in expo_ma_long.ma_histories.items():
        stockAxes.plot(history, label=f"EMA ({length})")

    stockAxes.plot(bb_1std.upper_band_history, label="Bollinger Upper (1 STD)")
    stockAxes.plot(bb_1std.lower_band_history, label="Bollinger Lower (1 STD)")

    stockAxes.legend(loc="best")
    algoAxes.legend(loc="lower left")

    plt.tight_layout()
    first_point = start_balance + data[0] * start_shares
    mpl.align.yaxes(stockAxes, data[0], algoAxes, first_point, 0.4)
    plt.show()

