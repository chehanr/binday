from statistics import mean, stdev, variance
from typing import List


def calc_mean(numbers: List[float]) -> float:
    return mean(numbers)


def calc_stdev(numbers: List[float]) -> float:
    return stdev(numbers)


def calc_variance(numbers: List[float]) -> float:
    return variance(numbers)
