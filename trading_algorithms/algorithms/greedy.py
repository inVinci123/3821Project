from typing import override

from algorithms.algorithm_class import TradingAlgorithm


class MaximallyGreedyAlgorithm(TradingAlgorithm):
    def __init__(self, starting_balance: float, starting_shares: float, trading_proportion: float = 0.5, trend_follow: bool = False):
        super().__init__(starting_balance, starting_shares)
        self.trading_proportion = trading_proportion
        self.trend_follow = trend_follow

    @override
    def give_data_point(self, stock_price: float):
        if len(self.seen_data_points) == 0:
            # Add the first data point to the algorithm
            self.seen_data_points.append(stock_price)
        last_data_point = self.seen_data_points[-1]
        current_balance = self.get_current_balance()
        current_shares = self.get_current_shares()
        super().give_data_point(stock_price)

        stock_rise = last_data_point < stock_price
        stock_fall = last_data_point > stock_price


        if stock_rise and not self.trend_follow or stock_fall and self.trend_follow:
            # Stock rise: Sell w of current shares
            selling_amount = current_shares * self.trading_proportion
            current_shares -= selling_amount
            current_balance += selling_amount * stock_price
            
        if stock_fall and not self.trend_follow or stock_rise and self.trend_follow:
            # Stock fall: Buy shares worth w of current balance
            buying_amount = current_balance * self.trading_proportion
            current_balance -= buying_amount
            current_shares += buying_amount / stock_price

        self.balance_history.append(current_balance)
        self.shares_history.append(current_shares)

