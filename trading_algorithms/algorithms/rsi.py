from algorithm_class import TradingAlgorithm
from typing import override

class RSIAlgorithm(TradingAlgorithm):
    def __init__(
        self,
        starting_balance: float,
        starting_shares: float,
        window_size: int = 14,
        oversold: float = 30.0,
        overbought: float = 70.0,
        trading_proportion: float = 0.5,
    ):
        super().__init__(starting_balance, starting_shares)
        self.window_size = window_size
        self.oversold = oversold
        self.overbought = overbought
        self.trading_proportion = trading_proportion
        self.rsi_history: list[float] = []

    @override
    def give_data_point(self, stock_price: float):
        super().give_data_point(stock_price)

        # Need at least window_size + 1 prices to compute RSI (we compute gains/losses between successive points)
        if len(self.seen_data_points) <= self.window_size:
            # not enough data yet
            self.rsi_history.append(50) # TODO: fix this in a not stupid way, probably just calculate with smaller window size
            self.balance_history.append(self.get_current_balance())
            self.shares_history.append(self.get_current_shares())
            return

        window = self.seen_data_points[-(self.window_size + 1):]  # last window_size+1 prices
        gains = 0.0
        losses = 0.0
        for i in range(1, len(window)):
            change = window[i] - window[i - 1]
            if change > 0:
                gains += change
            else:
                losses += -change

        avg_gain = gains / self.window_size
        avg_loss = losses / self.window_size

        # Avoid division by zero: if avg_loss == 0 then RSI is 100, if avg_gain == 0 RSI is 0
        if avg_loss == 0 and avg_gain == 0:
            rsi = 50.0
        elif avg_loss == 0:
            rsi = 100.0
        else:
            rs = avg_gain / avg_loss
            rsi = 100.0 - (100.0 / (1.0 + rs))

        self.rsi_history.append(rsi)

        current_balance = self.get_current_balance()
        current_shares = self.get_current_shares()

        # TODO: might want to make it so it only buys/sells when these lines are CROSSED, because can stay below for
        # extended periods of time
        # Trading logic: sell when overbought, buy when oversold
        if rsi >= self.overbought:
            selling_amount = current_shares * self.trading_proportion
            current_shares -= selling_amount
            current_balance += selling_amount * stock_price
        elif rsi <= self.oversold:
            buying_amount = current_balance * self.trading_proportion
            current_balance -= buying_amount
            # guard against division by zero (shouldn't happen for valid prices)
            if stock_price > 0:
                current_shares += buying_amount / stock_price

        self.balance_history.append(current_balance)
        self.shares_history.append(current_shares)
