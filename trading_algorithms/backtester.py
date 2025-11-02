import matplotlib.pyplot as plt
import mpl_axes_aligner as mpl
from typing import cast
from algorithm_class import TradingAlgorithm
from algorithm_factory import algorithm_create, AlgorithmTypes
from data_parser import parse_csv
from algorithms.true_optimal import get_optimal_worth_history
from metrics import sharpe, max_drawdown, calmar, cagr
from algorithms.simple_moving_average import SimpleMAAlgorithm
from algorithms.expo_moving_average import ExponentialMAAlgorithm
from algorithms.bollinger import BollingerBandsAlgorithm
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

    fig, stockAxes = plt.subplots()
    plt.title(stock)
    plt.xlabel("Days since start")
    stockAxes.set_ylabel("Stock Value")
    stockAxes.plot(data, 'k-+')
    stockAxes.set_xlim(0, len(data) - 1)

    print(f"\n=== {stock} ===")

    random_long = algorithm_create(AlgorithmTypes.RANDOM_CHOICE, start_balance, start_shares, [0.3, (0.4, 0.4)])
    simple_ma_long = algorithm_create(AlgorithmTypes.SIMPLE_MA, start_balance, start_shares)
    expo_ma_long = algorithm_create(AlgorithmTypes.EXPONENTIAL_MA, start_balance, start_shares, [1.0, (5, 21)])
    expo_ma_long2 = algorithm_create(AlgorithmTypes.EXPONENTIAL_MA, start_balance, start_shares, [1.0, (10, 20, 50)])
    bb_1std = BollingerBandsAlgorithm(start_balance, start_shares, num_std_dev=1.0)
    bb_2std = BollingerBandsAlgorithm(start_balance, start_shares, num_std_dev=2.0)

    algoAxes = stockAxes.twinx()
    algoAxes.set_ylabel("Worth history")


    def run_backtest(algorithm, name):
        print(name)

        backtest(algorithm, data, False)
        print(
            f"Balance: {start_balance} -> {algorithm.get_current_balance():.03f}\n"
            f"Shares:  {start_shares} -> {algorithm.get_current_shares():.03f}   (at {data[-1]:.03f} each)\n"
            f"TWorth:  {start_value} ({data[0]:.03f}) -> {algorithm.get_current_worth(data[-1]):.03f}\n"
            f"Yearly Sharpe Ratio: {sharpe(algorithm.worth_history)}\n"
            f"CAGR: {cagr(algorithm.worth_history)}\n"
            f"Max Drawdown: {max_drawdown(algorithm.worth_history)}\n"
            f"Calmar Ratio: {calmar(algorithm.worth_history)}\n")


    algs = [
        (random_long, "RANDOM", "r"),
        (simple_ma_long, "SIMPLE MA (5, 21)", "y"),
        (expo_ma_long, "EXPO MA (5, 21)", "b"),
        (expo_ma_long2, "EXPO MA (10, 20, 50)", "m"),
        (bb_1std, "BOLLINGER 1STD", "g"),
        (bb_2std, "BOLLINGER 2STD", "c"),
    ]

    for alg in algs:
        run_backtest(*alg[:2])
        final_point = alg[0].get_current_worth(data[-1])
        final_data = alg[0].get_worth_history() + [final_point]
        algoAxes.plot(final_data, color=alg[2], linestyle="--", label=alg[1])

    # PPO ML Attempt
    ppo_data, ppo_long = ppo_ml_algorithm(stock.upper(), start_balance, time_period="10y", interval="1d", model="final_model", plot_graphs=False)

    data_len_discrepancy = len(data) - len(ppo_data)
    ppo_plot_data = [start_balance] * data_len_discrepancy + ppo_data

    algoAxes.plot(ppo_plot_data, color="orange", linestyle="--", label="PPO ML")
    print(
        f"PPO-ML\n"
        f"Balance: {ppo_long.initial_balance} -> {ppo_long.balance:.03f}\n"
        f"Shares:  0 -> {ppo_long.shares_held:.03f}   (at {data[-1]:.03f} each)\n"
        f"TWorth:  {ppo_long.initial_balance} ({data[0]:.03f}) -> {ppo_long.net_worth:.03f}\n"
        f"Yearly Sharpe Ratio: {sharpe(ppo_data)}\n"
        f"CAGR: {cagr(ppo_data)}\n"
        f"Max Drawdown: {max_drawdown(ppo_data)}\n"
        f"Calmar Ratio: {calmar(ppo_data)}\n")


    # ---------------------- PLOTTING INDICATORS ----------------------

    stockAxes_legend = ["Stock Value"]
    for length, history in cast(SimpleMAAlgorithm, simple_ma_long).ma_histories.items():
        stockAxes.plot(history, label=f"SMA ({length})")
    for length, history in cast(ExponentialMAAlgorithm, expo_ma_long).ma_histories.items():
        stockAxes.plot(history, label=f"EMA ({length})")
    for length, history in cast(ExponentialMAAlgorithm, expo_ma_long2).ma_histories.items():
        stockAxes.plot(history, label=f"EMA ({length})")
    
    stockAxes.plot(bb_1std.upper_band_history, label="Bollinger Upper (1 STD)")
    stockAxes.plot(bb_1std.lower_band_history, label="Bollinger Lower (1 STD)")


    algoAxes.legend(loc="lower left")
    stockAxes.legend(loc="best")

    plt.tight_layout()
    first_point = start_balance + data[0] * start_shares
    mpl.align.yaxes(stockAxes, data[0], algoAxes, first_point, 0.4)
    plt.show()

