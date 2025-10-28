from __future__ import annotations

from typing import Dict, List, Optional, Tuple


class Indicator:
    """Base indicator class. Subclasses keep internal histories and provide
    an update method that consumes the algorithm's seen data and appends
    new indicator values to their histories.
    """

    def update(self, seen_data_points: List[float]):
        raise NotImplementedError()


class SimpleMovingAverageIndicator(Indicator):
    def __init__(self, ma_lengths: List[int]):
        self.ma_lengths = ma_lengths
        self.ma_histories: Dict[int, List[float]] = {l: [] for l in ma_lengths}

    def update(self, seen_data_points: List[float]):
        if not seen_data_points:
            return
        latest = seen_data_points[-1]
        for length, history in self.ma_histories.items():
            # replicate the previous in-algorithm logic for consistency
            if len(history) <= length:
                considered_history = seen_data_points[-length:]
                considered_length = len(considered_history)
                history.append(sum(considered_history) / considered_length)
            else:
                new_sma = history[-1] + (latest - seen_data_points[-1 - length]) / length
                history.append(new_sma)


class ExponentialMovingAverageIndicator(Indicator):
    def __init__(self, ma_lengths: List[int], smoothing_factor: float = 2.0):
        self.ma_lengths = ma_lengths
        self.smoothing_factor = smoothing_factor
        self.ma_histories: Dict[int, List[float]] = {l: [] for l in ma_lengths}

    def update(self, seen_data_points: List[float]):
        if not seen_data_points:
            return
        latest = seen_data_points[-1]
        for length, history in self.ma_histories.items():
            if len(history) == 0:
                history.append(latest)
                continue
            a = self.smoothing_factor / (1 + length)
            history.append(latest * a + history[-1] * (1 - a))


class BollingerBandsIndicator(Indicator):
    def __init__(self, window_size: int = 20, num_std_dev: float = 2.0):
        self.window_size = window_size
        self.num_std_dev = num_std_dev
        self.upper_band_history: List[float] = []
        self.lower_band_history: List[float] = []

    def update(self, seen_data_points: List[float]) -> Optional[Tuple[float, float]]:
        if len(seen_data_points) < self.window_size:
            return None
        window = seen_data_points[-self.window_size:]
        mean = sum(window) / self.window_size
        variance = sum((p - mean) ** 2 for p in window) / self.window_size
        std_dev = variance ** 0.5

        upper_band = mean + self.num_std_dev * std_dev
        lower_band = mean - self.num_std_dev * std_dev
        self.upper_band_history.append(upper_band)
        self.lower_band_history.append(lower_band)
        return upper_band, lower_band
