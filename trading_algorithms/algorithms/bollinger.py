from algorithm_class import TradingAlgorithm
from typing import override
from algorithms.indicators import BollingerBandsIndicator, SimpleMovingAverageIndicator


class BollingerBandsAlgorithm(TradingAlgorithm):
    def __init__(self, starting_balance: float, starting_shares: float, window_size: int = 20, num_std_dev: float = 2.0, trading_proportion: float = 0.5):
        super().__init__(starting_balance, starting_shares)
        self.window_size = window_size
        self.num_std_dev = num_std_dev
        self.trading_proportion = trading_proportion
        # use indicators for band calculations and the SMA centre-line
        self.indicator = BollingerBandsIndicator(window_size, num_std_dev)
        # SMA used to determine signals (use same window as Bollinger centre)
        self.sma = SimpleMovingAverageIndicator(window_size)
        # expose band histories for external code compatibility
        self.upper_band_history = self.indicator.upper_band_history
        self.lower_band_history = self.indicator.lower_band_history

    @override
    def give_data_point(self, stock_price: float):
        super().give_data_point(stock_price)

        # update both indicator histories
        bands = self.indicator.update(self.seen_data_points)
        self.sma.update(self.seen_data_points)

        if bands is None or not self.sma.history:
            # Not enough data to calculate Bollinger Bands
            self.balance_history.append(self.get_current_balance())
            self.shares_history.append(self.get_current_shares())
            return

        upper_band, lower_band = bands

        current_balance = self.get_current_balance()
        current_shares = self.get_current_shares()

        # Use the SMA value (centre line) to generate signals instead of raw price
        sma_value = self.sma.history[-1]

        if sma_value > upper_band:
            # Sell signal
            selling_amount = current_shares * self.trading_proportion
            current_shares -= selling_amount
            current_balance += selling_amount * stock_price
        elif sma_value < lower_band:
            # Buy signal
            buying_amount = current_balance * self.trading_proportion
            current_balance -= buying_amount
            current_shares += buying_amount / stock_price

        self.balance_history.append(current_balance)
        self.shares_history.append(current_shares)
