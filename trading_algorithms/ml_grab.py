from stable_baselines3 import PPO
from environmentcreator import EnhancedStockTradingEnvironment
from dataprocessor import StockDataProcessor


def ppo_ml_algorithm(ticker: str, starting_balance: float,
                     time_period: str = "1y", interval: str = "1d", model: str = "final_model", plot_graphs: bool = False):
    # Load local model
    # print("Loading model")
    model = PPO.load("models/" + model + ".zip")

    # The second returnee of PSP normalises the stock values by a significant margin.
    # e.g. 200 -> 1.2, because PPOs are generally sensitive
    # This also puts flags on certain indicators
    # print("Loading and processing stock data")
    _, le_data, _ = StockDataProcessor("dummy_stock", "dummy_cache").process_stocks_pipeline([ticker], time_period, interval)

    # print("Running predictions...")
    env = EnhancedStockTradingEnvironment(le_data, ticker, starting_balance, 
                                          transaction_cost=0., enable_logging=False)
    obs, _ = env.reset()

    action, _ = model.predict(obs, deterministic=True)
    info = {}
    while not info:
        obs, _, _, _, info = env.step(action)
        action, _ = model.predict(obs, deterministic=True)

    if plot_graphs:
        env.plot_performance()

    return [p["net_worth"] for p in env.portfolio_history], env

