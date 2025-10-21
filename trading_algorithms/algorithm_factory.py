from enum import Enum
from typing import Iterable

from algorithm_class import TradingAlgorithm
from algorithms.greedy import MaximallyGreedyAlgorithm
from algorithms.random_choice import RandomChoiceAlgorithm
from algorithms.best_after_n import BestAfterNAlgorithm
from algorithms.expo_moving_average import ExponentialMAAlgorithm


class AlgorithmTypes(Enum):
    MAXIMALLY_GREEDY = 0
    RANDOM_CHOICE = 1
    BEST_AFTER_N = 2
    EXPONENTIAL_MA = 3
    OTHER = 99


def algorithm_create(choice: AlgorithmTypes, starting_balance: float = 0, starting_shares: float = 0, meta_arguments: Iterable = []) -> TradingAlgorithm:
    match choice:
        case AlgorithmTypes.MAXIMALLY_GREEDY:
            return MaximallyGreedyAlgorithm(starting_balance, starting_shares, *meta_arguments)
        case AlgorithmTypes.RANDOM_CHOICE:
            return RandomChoiceAlgorithm(starting_balance, starting_shares, *meta_arguments)
        case AlgorithmTypes.BEST_AFTER_N:
            return BestAfterNAlgorithm(starting_balance, starting_shares, *meta_arguments)
        case AlgorithmTypes.EXPONENTIAL_MA:
            return ExponentialMAAlgorithm(starting_balance, starting_shares, *meta_arguments)
        case _:
            raise KeyError("Not yet implemented")

