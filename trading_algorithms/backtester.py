import matplotlib.pyplot as plt
import mpl_axes_aligner as mpl
from typing import cast
from algorithm_class import TradingAlgorithm
from algorithm_factory import algorithm_create, AlgorithmTypes
from data_parser import parse_csv
from metrics import sharpe, max_drawdown, calmar, cagr, average_trade
from algorithms.true_optimal import get_optimal_worth_history
from algorithms.simple_moving_average import SimpleMAAlgorithm
from algorithms.expo_moving_average import ExponentialMAAlgorithm
from algorithms.bollinger import BollingerBandsAlgorithm
from algorithms.rsi import RSIAlgorithm
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


test_ml = True
plot_out = False


bullish_stocks = ["AAPL","ALL.AX","AMZN","ANZ.AX","BTC-USD","BXB.AX","CBA.AX","COH.AX","COL.AX","FMG.AX","GMG.AX","GOOGL","MQG.AX","MSFT","NAB.AX","NEM.AX","NST.AX","NVDA","NWS.AX","PME.AX","QAN.AX","QBE.AX","REA.AX","RIO.AX","RMD.AX","SCG.AX","SIG.AX","STO.AX","SUN.AX","TCL.AX","TLS.AX","VAS.AX","WBC.AX","WES.AX","WTC.AX","XRO.AX","XYZ.AX"]

sideways_stocks = ["AMC.AX", "ASX.AX", "BHP.AX", "CSL.AX", "WDS.AX", "WOW.AX"]

testing_stocks = bullish_stocks

for stock in testing_stocks:
    data = parse_csv(stock.lower() + ".csv")
    # data = data * 10
    start_balance = 1000
    start_shares = 0
    true_optimal = get_optimal_worth_history(data, start_balance, start_shares)
    start_value = round(start_balance + start_shares * data[0], 3)

    fig, stock_axes = plt.subplots()
    # fig, (stock_axes, rsi_axes) = plt.subplots(2, 1, sharex=True,
    #                                           gridspec_kw={"height_ratios": [3, 1]}, figsize=(10, 6))
    plt.title(stock)
    plt.xlabel("Days since start")
    stock_axes.set_ylabel("Stock Value")
    stock_axes.plot(data, 'k-+')
    stock_axes.set_xlim(0, len(data) - 1)

    # rsi_axes.set_xlabel("Days since start")
    # rsi_axes.set_ylabel("RSI")
    # rsi_axes.set_ylim(0, 100)
    # rsi_axes.set_xlim(0, len(data) - 1)

    print(f"\n=== {stock} ===")

    greedy_long = algorithm_create(AlgorithmTypes.MAXIMALLY_GREEDY, start_balance, start_shares)
    random_long = algorithm_create(AlgorithmTypes.RANDOM_CHOICE, start_balance, start_shares, [0.3, (0.4, 0.4)])
    best_after_long = algorithm_create(AlgorithmTypes.BEST_AFTER_N, start_balance, start_shares)
    simple_ma_long = algorithm_create(AlgorithmTypes.SIMPLE_MA, start_balance, start_shares, [1.0, (5, 21)])
    expo_ma_long = algorithm_create(AlgorithmTypes.EXPONENTIAL_MA, start_balance, start_shares, [1.0, (10, 20, 50)])
    bb_1std = algorithm_create(AlgorithmTypes.BBANDS, start_balance, start_shares, (20, 1.0))
    bb_2std = algorithm_create(AlgorithmTypes.BBANDS, start_balance, start_shares, (20, 2.0))
    rsi_algo = algorithm_create(AlgorithmTypes.RSI, start_balance, start_shares, (50,))

    algo_axes = stock_axes.twinx()
    algo_axes.set_ylabel("Worth history")


    def run_backtest(algorithm, name):
        backtest(algorithm, data, False)
        print('#', name)
        print(
            f"Balance: {start_balance} -> {algorithm.get_current_balance():.03f}\n"
            f"Shares:  {start_shares} -> {algorithm.get_current_shares():.03f}   (at {data[-1]:.03f} each)\n"
            f"TWorth:  {start_value} ({data[0]:.03f}) -> {algorithm.get_current_worth(data[-1]):.03f}\n"
            f"Yearly Sharpe Ratio: {sharpe(algorithm.worth_history)}\n"
            f"CAGR: {cagr(algorithm.worth_history)}\n"
            f"Max Drawdown: {max_drawdown(algorithm.worth_history)}\n"
            f"Calmar Ratio: {calmar(algorithm.worth_history)}\n"
            f"Average Trade: {average_trade(algorithm.worth_history, algorithm.balance_history)}\n")


    algs = [
        (greedy_long, "GREEDY"),
        (random_long, "RANDOM"),
        (best_after_long, "BEST AFTER 10"),
        (simple_ma_long, "SIMPLE MA (5, 21)"),
        (expo_ma_long, "EXPO MA (10, 20, 50)"),
        (bb_1std, "BOLLINGER 1STD"),
        (bb_2std, "BOLLINGER 2STD"),
        (rsi_algo, "RSI"),
    ]

    for alg in algs:
        run_backtest(*alg[:2])
        final_point = alg[0].get_current_worth(data[-1])
        final_data = alg[0].get_worth_history() + [final_point]
        algo_axes.plot(final_data, linestyle="--", label=alg[1])

    # ---------------------- PLOTTING INDICATORS ----------------------

    stock_axes_legend = ["Stock Value"]
    # for length, history in cast(SimpleMAAlgorithm, simple_ma_long).ma_histories.items():
    #     stock_axes.plot(history, label=f"SMA ({length})")
    # for length, history in cast(ExponentialMAAlgorithm, expo_ma_long).ma_histories.items():
    #     stock_axes.plot(history, label=f"EMA ({length})")
    
    # stock_axes.plot(bb_1std.upper_band_history, label="Bollinger Upper (1 STD)")
    # stock_axes.plot(bb_1std.lower_band_history, label="Bollinger Lower (1 STD)")


    # rsi_algo = cast(RSIAlgorithm, rsi_algo)
    # rsi_axes.plot(rsi_algo.rsi_history, label="RSI")
    # # Draw common RSI threshold lines
    # rsi_axes.axhline(rsi_algo.overbought, color="red", linestyle="--", linewidth=0.7, label="Overbought")
    # rsi_axes.axhline(rsi_algo.oversold, color="green", linestyle="--", linewidth=0.7, label="Oversold")
    # rsi_axes.legend(loc="lower right")

    # ---------------------------------------------------------------


    if test_ml:
        # PPO ML Attempt
        ppo_data, ppo_long = ppo_ml_algorithm(stock.upper(), start_balance, time_period="10y", interval="1d", model="final_model", plot_graphs=False)

        data_len_discrepancy = len(data) - len(ppo_data)
        ppo_plot_data = [start_balance] * data_len_discrepancy + ppo_data
        algo_axes.plot(ppo_plot_data, color="cyan", linestyle="--", label="PPO ML")

        ppo_bal_history = [p['balance'] for p in ppo_long.portfolio_history]
        print(
            f"# PPO-ML\n"
            f"Balance: {ppo_long.initial_balance} -> {ppo_long.balance:.03f}\n"
            f"Shares:  0 -> {ppo_long.shares_held:.03f}   (at {data[-1]:.03f} each)\n"
            f"TWorth:  {ppo_long.initial_balance} ({data[0]:.03f}) -> {ppo_long.net_worth:.03f}\n"
            f"Yearly Sharpe Ratio: {sharpe(ppo_data)}\n"
            f"CAGR: {cagr(ppo_data)}\n"
            f"Max Drawdown: {max_drawdown(ppo_data)}\n"
            f"Calmar Ratio: {calmar(ppo_data)}\n"
            f"Average Trade: {average_trade(ppo_data, ppo_bal_history)}\n")


    # Finishing plotting
    algo_axes.legend(loc="lower left")
    stock_axes.legend(loc="best")

    if plot_out:
        plt.tight_layout()
        first_worth = start_balance + data[0] * start_shares
        mpl.align.yaxes(stock_axes, data[0], algo_axes, first_worth, 0.3)
        plt.show()

