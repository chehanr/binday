from typing import List


def parse_serial_str(data: str) -> List[str]:
    return data.strip().split(";")


def get_bin_level(bin_height: int, sonar_reading: int = 0) -> int:
    level = bin_height - sonar_reading

    return level if level >= 0 else 0


def get_bin_level_perc(bin_height: int, sonar_reading: int = 0) -> float:
    return (get_bin_level(bin_height, sonar_reading) / bin_height) * 100
