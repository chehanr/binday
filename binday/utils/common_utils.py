from datetime import datetime

from binday.server.models.bin_day import DayIndex


def get_millis_time(date_time: datetime) -> float:
    return date_time.timestamp() * 1000


def day_index_to_int(day_index: DayIndex) -> int:
    if day_index == DayIndex.MONDAY:
        return 0
    if day_index == DayIndex.TUESDAY:
        return 1
    if day_index == DayIndex.WEDNESDAY:
        return 2
    if day_index == DayIndex.THURSDAY:
        return 3
    if day_index == DayIndex.FRIDAY:
        return 4
    if day_index == DayIndex.SATURDAY:
        return 5
    if day_index == DayIndex.SUNDAY:
        return 6

    raise IndexError
