from collections import defaultdict
from datetime import datetime
from math import ceil
from typing import DefaultDict, List

from binday.server.models.base import Base
from binday.server.models.bin_day import CollectionFrequency, DayIndex
from binday.utils.common_utils import day_index_to_int


def parse_serial_str(data: str) -> List[str]:
    return data.strip().split(";")


def get_bin_level(bin_height: int, sonar_reading: int = 0) -> int:
    level = bin_height - sonar_reading

    return level if level >= 0 else 0


def get_bin_level_perc(bin_height: int, sonar_reading: int = 0) -> float:
    return (get_bin_level(bin_height, sonar_reading) / bin_height) * 100


def check_binday(
    dt: datetime, bin_day_index: DayIndex, bin_day_freq: CollectionFrequency
) -> bool:
    week_day = dt.weekday()

    if week_day != day_index_to_int(bin_day_index):
        return False

    first_day = dt.replace(day=1)
    dom = dt.day
    adjusted_dom = dom + first_day.weekday()

    week_index = int(ceil(adjusted_dom / 7.0))

    if bin_day_freq == CollectionFrequency.WEEKLY:
        return True
    if bin_day_freq == CollectionFrequency.FORTNIGHTLY:
        return True if week_index in [0, 2] else False
    if bin_day_freq == CollectionFrequency.MONTHLY:
        return True if week_index == 0 else False

    return False


def group_by_date_created(data: List[Base]) -> DefaultDict[datetime, List]:
    groups = defaultdict(list)

    for d in data:
        groups[d.date_created.date()].append(d)

    return groups
