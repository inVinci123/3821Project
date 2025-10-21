import matplotlib.pyplot as plt
import mpl_axes_aligner as mpl
from algorithm_class import TradingAlgorithm
from algorithm_factory import algorithm_create, AlgorithmTypes
from data_parser import parse_csv
from algorithms.true_optimal import get_optimal_worth_history


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
testing_stocks = ["dowjonesmonthly100y"]
greedy_wins = 0
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
    ax1.legend("Stock Value")
    ax1.set_xlim(0, len(data) - 1)

    print(f"\n=== {stock} ===")


    print("GREEDY")

    greedy_long = algorithm_create(AlgorithmTypes.MAXIMALLY_GREEDY, start_balance, start_shares)
    random_long = algorithm_create(AlgorithmTypes.RANDOM_CHOICE, start_balance, start_shares, [0.3, (0.4, 0.4)])
    best_after_long = algorithm_create(AlgorithmTypes.BEST_AFTER_N, start_balance, start_shares)
    expo_ma_long = algorithm_create(AlgorithmTypes.EXPONENTIAL_MA, start_balance, start_shares, [1.0, (5, 21)])
    expo_ma_long2 = algorithm_create(AlgorithmTypes.EXPONENTIAL_MA, start_balance, start_shares)

    backtest(greedy_long, data, False)
    greedy_final = greedy_long.get_current_worth(data[-1])
    greedy_data = greedy_long.get_worth_history() + [greedy_final]
    print(         
        f"Balance: {start_balance} -> {greedy_long.get_current_balance():.03f}\n"
        f"Shares:  {start_balance} -> {greedy_long.get_current_shares():.03f}   (at {data[-1]:.03f} each)\n"
        f"TWorth:  {start_value} ({data[0]:.03f}) -> {greedy_long.get_current_worth(data[-1]):.03f}")

    print("\nRANDOM")

    backtest(random_long, data, False)
    random_final = random_long.get_current_worth(data[-1])
    random_data = random_long.get_worth_history() + [random_final]
    print(         
        f"Balance: {start_balance} -> {random_long.get_current_balance():.03f}\n"
        f"Shares:  {start_balance} -> {random_long.get_current_shares():.03f}   (at {data[-1]:.03f} each)\n"
        f"TWorth:  {start_value} ({data[0]:.03f}) -> {random_long.get_current_worth(data[-1]):.03f}")

    print("\nBEST AFTER N")
    backtest(best_after_long, data, False)
    best_after_final = best_after_long.get_current_worth(data[-1])
    best_after_data = best_after_long.get_worth_history() + [best_after_final]
    print(         
        f"Balance: {start_balance} -> {best_after_long.get_current_balance():.03f}\n"
        f"Shares:  {start_balance} -> {best_after_long.get_current_shares():.03f}   (at {data[-1]:.03f} each)\n"
        f"TWorth:  {start_value} ({data[0]:.03f}) -> {best_after_long.get_current_worth(data[-1]):.03f}")

    print("\nEXPONENTIAL MA")
    backtest(expo_ma_long, data, False)
    backtest(expo_ma_long2, data, False)
    expo_ma_final = expo_ma_long.get_current_worth(data[-1])
    expo_ma_final2 = expo_ma_long2.get_current_worth(data[-1])
    expo_ma_data = expo_ma_long.get_worth_history() + [expo_ma_final]
    expo_ma_data2 = expo_ma_long2.get_worth_history() + [expo_ma_final2]
    print(         
        f"Balance: {start_balance} -> {expo_ma_long.get_current_balance():.03f}\n"
        f"Shares:  {start_balance} -> {expo_ma_long.get_current_shares():.03f}   (at {data[-1]:.03f} each)\n"
        f"TWorth:  {start_value} ({data[0]:.03f}) -> {expo_ma_long.get_current_worth(data[-1]):.03f}")

    ax2 = ax1.twinx()
    ax2.plot(true_optimal, 'cyan')

    ax2.set_ylabel("Worth history")
    ax2.plot(greedy_data, 'r--')
    ax2.plot(random_data, 'b--')
    ax2.plot(best_after_data, 'g--')
    ax2.plot(expo_ma_data, 'y--')
    ax2.plot(expo_ma_data2, 'm--')
    ax2.legend(["Optimal", "Greedy", "Random", "Best after n", "Expo MA (5, 21)", "Expo MA (8, 13, 21)"])

    for history in expo_ma_long.ma_histories.values():
        ax1.plot(history)
    for history in expo_ma_long2.ma_histories.values():
        ax1.plot(history)

    plt.tight_layout()
    mpl.align.yaxes(ax1, data[0], ax2, greedy_data[0], 0.4)
    plt.show()
    if greedy_final >= random_final and greedy_final > best_after_final:
        greedy_wins += 1

print("Greedy won", greedy_wins, "out of", len(testing_stocks))

