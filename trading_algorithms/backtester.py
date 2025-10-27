import matplotlib.pyplot as plt
import mpl_axes_aligner as mpl
from algorithm_class import TradingAlgorithm
from algorithm_factory import algorithm_create, AlgorithmTypes
from data_parser import parse_csv
from algorithms.true_optimal import get_optimal_worth_history
from ml_grab import ppo_ml_algorithm


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
testing_stocks = ["MSFT", "AAPL", "NVDA", "NAB.AX", "BTC-USD", "CBA.AX", "ANZ.AX"]
# testing_stocks = ["dowjonesmonthly100y", "ASX.AX"]
for stock in testing_stocks:
    data = parse_csv(stock.lower() + ".csv")
    # data = data * 10
    start_balance = 1000
    start_shares = 0
    true_optimal = get_optimal_worth_history(data, start_balance, start_shares)
    start_value = round(start_balance + start_shares * data[0], 3)

    fig, ax1 = plt.subplots()
    plt.title(stock)
    plt.xlabel("Days since start")
    ax1.set_ylabel("Stock Value")
    ax1.plot(data, 'k-+')
    ax1.set_xlim(0, len(data) - 1)

    print(f"\n=== {stock} ===")

    random_long = algorithm_create(AlgorithmTypes.RANDOM_CHOICE, start_balance, start_shares, [0.3, (0.4, 0.4)])
    expo_ma_long = algorithm_create(AlgorithmTypes.EXPONENTIAL_MA, start_balance, start_shares, [1.0, (5, 21)])
    expo_ma_long2 = algorithm_create(AlgorithmTypes.EXPONENTIAL_MA, start_balance, start_shares)
    simple_ma_long = algorithm_create(AlgorithmTypes.SIMPLE_MA, start_balance, start_shares, [1.0, (5, 21)])
    simple_ma_long2 = algorithm_create(AlgorithmTypes.SIMPLE_MA, start_balance, start_shares)

    ax2 = ax1.twinx()
    ax2.set_ylabel("Worth history")

    def run_backtest(algorithm, name):
        print(name)

        backtest(algorithm, data, False)
        print(
            f"Balance: {start_balance} -> {algorithm.get_current_balance():.03f}\n"
            f"Shares:  {start_balance} -> {algorithm.get_current_shares():.03f}   (at {data[-1]:.03f} each)\n"
            f"TWorth:  {start_value} ({data[0]:.03f}) -> {algorithm.get_current_worth(data[-1]):.03f}\n")


    algs = [
        (random_long, "RANDOM", "r--"),
        (expo_ma_long, "EXPO MA (5, 21)", "b--"),
        (expo_ma_long2, "EXPO MA (8, 13, 21)", "c--"),
        (simple_ma_long, "SIMPLE MA (5, 21)", "y--"),
        (simple_ma_long2, "SIMPLE MA (8, 13, 21)", "m--")
    ]

    for alg in algs:
        run_backtest(*alg[:2])
        final_point = alg[0].get_current_worth(data[-1])
        final_data = alg[0].get_worth_history() + [final_point]
        ax2.plot(final_data, alg[2], label=alg[1])

    # PPO ML Attempt
    ppo_long = ppo_ml_algorithm(stock.upper(), start_balance, time_period="10y", interval="1d", model="final_model", plot_graphs=False)
    ax2.plot(final_data, "g--", label="PPO ML")


    ax1_legend = ["Stock Value"]
    for length, history in simple_ma_long.ma_histories.items():
        ax1.plot(history, label=f"SMA ({length})")
    for length, history in expo_ma_long.ma_histories.items():
        ax1.plot(history, label=f"EMA ({length})")

    ax1.legend(loc="best")
    ax2.legend(loc="lower left")

    plt.tight_layout()
    first_point = start_balance + data[0] * start_shares
    mpl.align.yaxes(ax1, data[0], ax2, first_point, 0.4)
    plt.show()

