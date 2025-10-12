from typing import override
from random import randint

from algorithm_class import TradingAlgorithm


class RandomChoiceAlgorithm(TradingAlgorithm):
    def __init__(self, starting_balance: float, starting_shares: float, trading_proportion: float = 0.3):
        super().__init__(starting_balance, starting_shares)
        # Trading proportion w
        self.trading_proportion = trading_proportion

    @override
    def give_data_point(self, stock_price: float):
        super().give_data_point(stock_price)

        current_balance = self.get_current_balance()
        current_shares = self.get_current_shares()

        match randint(1, 3):
            case 1:
                # Random sell
                selling_amount = current_shares * self.trading_proportion
                current_shares -= selling_amount
                current_balance += selling_amount * stock_price
            case 2:
                # Random buy
                buying_amount = current_balance * self.trading_proportion
                current_balance -= buying_amount
                current_shares += buying_amount / stock_price
            case 3:
                # Do nothing
                pass

        self.balance_history.append(current_balance)
        self.shares_history.append(current_shares)

