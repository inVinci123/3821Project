from stable_baselines3 import PPO
from ppo_ml_files.environmentcreator import ActionType, EnhancedStockTradingEnvironment
from ppo_ml_files.dataprocessor import StockDataProcessor
import yfinance


def ppo_ml_algorithm(ticker: str, starting_balance: float,
                     time_period: str = "5y", interval: str = "1d", model: str = "final_model", plot_graphs: bool = False):
    # Load local model
    # print("Loading model")
    model = PPO.load("models/" + model + ".zip")

    # The second returnee of PSP normalises the stock values by a significant margin.
    # e.g. 200 -> 1.2, because PPOs are generally sensitive
    # This also puts flags on certain indicators
    # print("Loading and processing stock data")
    _, le_data, _ = StockDataProcessor("dummy_stock", "dummy_cache").process_stocks_pipeline([ticker], time_period, interval)

    yticker = yfinance.Ticker(ticker)
    hist_data = yticker.history(period="5y")
    data = hist_data.to_csv(date_format="%d/%m/%y")

    data_points = []
    for line in data.strip().split('\n'):
        line = line.strip()
        if line.startswith("Date"):
            continue
        components = line.split(',')
        key_points = (float(x) for x in components[1:5])
        data_points.append(sum(key_points) / 4)

    balance_history = [starting_balance]
    shares_history = [0]
    net_worth_history = [starting_balance]

    # print("Running predictions...")
    env = EnhancedStockTradingEnvironment(le_data, ticker, starting_balance, 
                                          transaction_cost=0., enable_logging=False)
    obs, _ = env.reset()

    action, _ = model.predict(obs, deterministic=True)
    info = {}
    i = 0
    while not info:
        obs, _, _, _, info = env.step(action)
        action, _ = model.predict(obs, deterministic=True)

        current_balance = balance_history[-1]
        current_shares = shares_history[-1]

        if round(action[0]) == ActionType.BUY:
            amount_to_spend = current_balance * action[1]
            current_balance -= amount_to_spend
            current_shares += amount_to_spend / data_points[i]
        elif round(action[0]) == ActionType.SELL:
            amount_to_sell = current_shares * action[1]
            current_shares -= amount_to_sell
            current_balance += amount_to_sell * data_points[i]
        else:
            pass

        i += 1
        balance_history.append(current_balance)
        shares_history.append(current_shares)
        net_worth_history.append(current_balance + data_points[i] * current_shares)

    if plot_graphs:
        env.plot_performance()

    return net_worth_history, env

