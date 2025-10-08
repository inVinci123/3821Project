from enum import Enum

from algorithm_class import TradingAlgorithm
from algorithms.greedy import MaximallyGreedyAlgorithm


class AlgorithmTypes(Enum):
    MAXIMALLY_GREEDY = 0
    RANDOM_CHOICE = 1
    OTHER = 2


def algorithm_create(choice: AlgorithmTypes, starting_balance: float = 0, starting_shares: float = 0) -> TradingAlgorithm:
    match choice:
        case AlgorithmTypes.MAXIMALLY_GREEDY:
            return MaximallyGreedyAlgorithm(starting_balance, starting_shares)
        case _:
            raise KeyError("Not yet implemented")

