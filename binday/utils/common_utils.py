from datetime import datetime


def get_millis_time(date_time: datetime) -> float:
    return date_time.timestamp() * 1000
