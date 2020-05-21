from typing import List


def parse_serial_str(data: str) -> List[str]:
    return data.strip().split(";")


def get_bin_level(bin_height: int, sonar_reading: int) -> int:
    return bin_height - sonar_reading


def get_bin_level_perc(bin_height: int, sonar_reading: int) -> float:
    return (get_bin_level(bin_height, sonar_reading) / bin_height) * 100
