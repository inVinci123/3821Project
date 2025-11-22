from typing import override

from algorithms.algorithm_class import TradingAlgorithm


class SimpleMAAlgorithm(TradingAlgorithm):
    def __init__(self, starting_balance: float, starting_shares: float, trading_proportion: float = 1.0,
                 ma_lengths: list[int] = [8, 13, 21]):
        super().__init__(starting_balance, starting_shares)
        self.trading_proportion = trading_proportion
        self.ma_lengths = ma_lengths
        self.ma_histories: dict[int, list[float]] = {l: [] for l in ma_lengths}
        self.selling: bool = starting_shares > 0
    

    @override
    def give_data_point(self, stock_price: float):
        super().give_data_point(stock_price)
        for length, history in self.ma_histories.items():
            # Calculate new moving average
            if len(history) <= length:
                considered_history = self.seen_data_points[-length:]
                considered_length = len(considered_history)
                history.append(sum(considered_history) / considered_length)
            else:
                # new_sma = (x2 + ... + xn+1) / n
                # = (x2 + ... + xn + xn+1 + (x1 - x1)) / n
                # = (x1 + ... + xn) / n + (xn+1 - x1) / n
                # = prev_sma + (new - first_considered) / n
                new_sma = history[-1] + (stock_price - self.seen_data_points[-1 - length]) / length
                history.append(new_sma)

        current_balance = self.get_current_balance()
        current_shares = self.get_current_shares()

        if self.selling:
            # Looking to sell in a falling trend
            # Looking for low-SMA < ... < high-SMA
            will_sell = True
            for i in range(len(self.ma_histories.keys()) - 1):
                lower_length = list(self.ma_histories.keys())[i]
                higher_length = list(self.ma_histories.keys())[i + 1]
                if self.ma_histories[lower_length][-1] >= self.ma_histories[higher_length][-1]:
                    will_sell = False
                    break

            if will_sell:
                current_balance += current_shares * stock_price
                current_shares = 0
                self.selling = False
        else:
            # Looking to buy in a growing trend
            # Looking for low-SMA > ... > high-SMA
            will_buy = True
            for i in range(len(self.ma_histories.keys()) - 1):
                lower_length = list(self.ma_histories.keys())[i]
                higher_length = list(self.ma_histories.keys())[i + 1]
                if self.ma_histories[lower_length][-1] <= self.ma_histories[higher_length][-1]:
                    will_buy = False
                    break

            if will_buy:
                buying_shares = current_balance * self.trading_proportion / stock_price
                current_shares += buying_shares
                current_balance -= buying_shares * stock_price
                self.selling = True

        self.balance_history.append(current_balance)
        self.shares_history.append(current_shares)

