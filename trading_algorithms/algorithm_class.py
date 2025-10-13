from abc import ABC, abstractmethod

class TradingAlgorithm(ABC):
    def __init__(self, starting_balance: float, starting_shares: float):
        self.current_index: int = 0
        self.seen_data_points: list[float] = []
        self.balance_history: list[float] = [starting_balance]
        self.shares_history: list[float] = [starting_shares]
        self.worth_history: list[float] = []

    @abstractmethod
    def give_data_point(self, stock_price: float):
        # Override this in subclasses
        # Call super first
        if len(self.seen_data_points) > 0:
            previous_stock_price = self.seen_data_points[-1]
            previous_worth = self.get_current_worth(previous_stock_price)
            self.worth_history.append(previous_worth)
        self.seen_data_points.append(stock_price)
        self.current_index += 1


    def get_current_index(self) -> int:
        return self.current_index

    def get_current_balance(self) -> float:
        return self.balance_history[-1]

    def get_current_shares(self) -> float:
        return self.shares_history[-1]

    def get_current_worth(self, stock_price: float) -> float:
        return self.balance_history[-1] + stock_price * self.shares_history[-1]


    def get_balance_history(self) -> list[float]:
        return self.balance_history

    def get_shares_history(self) -> list[float]:
        return self.shares_history

    def get_worth_history(self) -> list[float]:
        return self.worth_history

