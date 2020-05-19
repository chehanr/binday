from typing import List


def parse_serial_str(data: str) -> List[str]:
    return data.strip().split(";")
