from typing import override

from algorithm_class import TradingAlgorithm


class BestAfterNAlgorithm(TradingAlgorithm):
    def __init__(self, starting_balance: float, starting_shares: float, searching_number: int = 10):
        super().__init__(starting_balance, starting_shares)
        self.searching_number: int = searching_number
        self.considering_from: int = 0
        self.selling: bool = starting_shares > 0

    @override
    def give_data_point(self, stock_price: float):
        super().give_data_point(stock_price)
        current_balance = self.get_current_balance()
        current_shares = self.get_current_shares()

        actionable = self.current_index - self.considering_from > self.searching_number
        if actionable:
            # Will only consider doing an action after n prices have been considered
            if self.selling:
                if stock_price >= max(self.seen_data_points[self.considering_from:]):
                    # Highest stock price after the first n prices considered
                    current_balance += current_shares * stock_price
                    current_shares = 0
                    self.considering_from = self.current_index
                    self.selling = False
            else:
                if stock_price <= min(self.seen_data_points[self.considering_from:]):
                    # Lowest stock price after the first n prices considered
                    current_shares += current_balance / stock_price
                    current_balance = 0
                    self.considering_from = self.current_index
                    self.selling = True

        self.balance_history.append(current_balance)
        self.shares_history.append(current_shares)

