from algorithm_class import TradingAlgorithm
from typing import override

class BollingerBandsAlgorithm(TradingAlgorithm):
    def __init__(self, starting_balance: float, starting_shares: float, window_size: int = 20, num_std_dev: float = 2.0, trading_proportion: float = 0.5):
        super().__init__(starting_balance, starting_shares)
        self.window_size = window_size
        self.num_std_dev = num_std_dev
        self.trading_proportion = trading_proportion
        self.upper_band_history: list[float] = []
        self.lower_band_history: list[float] = []

    @override
    def give_data_point(self, stock_price: float):
        super().give_data_point(stock_price)

        window = self.seen_data_points[-self.window_size:]
        mean = sum(window) / len(window)
        variance = sum((p - mean) ** 2 for p in window) / len(window)
        std_dev = variance ** 0.5

        upper_band = mean + self.num_std_dev * std_dev
        lower_band = mean - self.num_std_dev * std_dev
        self.upper_band_history.append(upper_band)
        self.lower_band_history.append(lower_band)

        if len(self.seen_data_points) < self.window_size:
            # Not enough data to make informed actioms with Bollinger bands
            self.balance_history.append(self.get_current_balance())
            self.shares_history.append(self.get_current_shares())
            return

        current_balance = self.get_current_balance()
        current_shares = self.get_current_shares()

        if stock_price > upper_band:
            # Sell signal
            selling_amount = current_shares * self.trading_proportion
            current_shares -= selling_amount
            current_balance += selling_amount * stock_price
        elif stock_price < lower_band:
            # Buy signal
            buying_amount = current_balance * self.trading_proportion
            current_balance -= buying_amount
            current_shares += buying_amount / stock_price

        self.balance_history.append(current_balance)
        self.shares_history.append(current_shares)
