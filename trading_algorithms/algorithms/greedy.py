from typing import override

from algorithm_class import TradingAlgorithm


class MaximallyGreedyAlgorithm(TradingAlgorithm):
    def __init__(self, starting_balance: float, starting_shares: float):
        super().__init__(starting_balance, starting_shares)

    @override
    def give_data_point(self, stock_price: float):
        if len(self.seen_data_points) == 0:
            # Add the first data point to the algorithm
            self.seen_data_points.append(stock_price)
        last_data_point = self.seen_data_points[-1]
        current_balance = self.get_current_balance()
        current_shares = self.get_current_shares()
        super().give_data_point(stock_price)

        if last_data_point < stock_price:
            # Stock rise: Sell half of current shares
            current_shares *= 0.5
            current_balance += current_shares * stock_price
            
        elif last_data_point > stock_price:
            # Stock fall: Buy shares worth half of current balance
            current_balance *= 0.5
            current_shares += current_balance / stock_price

        self.balance_history.append(current_balance)
        self.shares_history.append(current_shares)

