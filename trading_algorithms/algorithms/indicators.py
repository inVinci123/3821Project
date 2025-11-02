from __future__ import annotations

from typing import List, Optional, Tuple
from abc import ABC, abstractmethod


class Indicator(ABC):
    """Base indicator class. Subclasses should implement update(seen_data_points).

    Each Indicator instance represents a single series (e.g. a 21-day SMA).
    """

    @abstractmethod
    def update(self, seen_data_points: List[float]):
        pass


class SimpleMovingAverageIndicator(Indicator):
    def __init__(self, length: int):
        self.length = length
        self.history: List[float] = []

    def update(self, seen_data_points: List[float]):
        if not seen_data_points:
            return
        
        used_length = min(len(seen_data_points), self.length)
        window = seen_data_points[-used_length:]
        sma = sum(window) / len(window)
        self.history.append(sma)


class ExponentialMovingAverageIndicator(Indicator):
    def __init__(self, length: int, smoothing_factor: float = 2.0):
        self.length = length
        self.smoothing_factor = smoothing_factor
        self.history: List[float] = []

    def update(self, seen_data_points: List[float]):
        if not seen_data_points:
            return
        latest = seen_data_points[-1]
        history = self.history
        if len(history) == 0:
            history.append(latest)
            return
        a = self.smoothing_factor / (1 + self.length)
        history.append(latest * a + history[-1] * (1 - a))


class BollingerBandsIndicator(Indicator):
    def __init__(self, window_size: int = 20, num_std_dev: float = 2.0):
        self.window_size = window_size
        self.num_std_dev = num_std_dev
        self.upper_band_history: List[float] = []
        self.lower_band_history: List[float] = []

    def update(self, seen_data_points: List[float]) -> Optional[Tuple[float, float]]:
        size_used = min(len(seen_data_points), self.window_size)
        window = seen_data_points[-size_used:]
        mean = sum(window) / size_used
        variance = sum((p - mean) ** 2 for p in window) / size_used
        std_dev = variance ** 0.5

        upper_band = mean + self.num_std_dev * std_dev
        lower_band = mean - self.num_std_dev * std_dev
        self.upper_band_history.append(upper_band)
        self.lower_band_history.append(lower_band)
        return upper_band, lower_band
