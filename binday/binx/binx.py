from dataclasses import dataclass
from typing import Optional

from binday.boards.board import Board
from binday.utils.bin_utils import parse_serial_str


@dataclass
class BinX:
    name: str
    sonar_id: str
    led_id: str


class BinActions:
    def __init__(self, board: Board, binx: BinX):
        self.board = board
        self.binx = binx

    def query_bin_sonar(self) -> None:
        self.board.write(f"SONAR;{self.binx.sonar_id};QUERY\n".encode("utf-8"))

    def query_bin_led(self) -> None:
        self.board.write(f"LED;{self.binx.led_id};QUERY\n".encode("utf-8"))

    def turn_bin_led_on(self) -> None:
        self.board.write(f"LED;{self.binx.led_id};ON\n".encode("utf-8"))

    def turn_bin_led_off(self) -> None:
        self.board.write(f"LED;{self.binx.led_id};OFF\n".encode("utf-8"))

    def get_bin_sonar(self) -> Optional[int]:
        self.query_bin_sonar()

        data = self.board.readline()

        if data == b"":
            return None

        p_data = parse_serial_str(data.decode("utf-8"))

        if len(p_data) == 0:
            return None

        if p_data[0] == "SONAR" and p_data[1] == self.binx.sonar_id:
            return int(p_data[2])

        return None

    def get_bin_led_status(self) -> Optional[bool]:
        self.query_bin_led()

        data = self.board.readline()

        if data == b"":
            return None

        p_data = parse_serial_str(data.decode("utf-8"))

        if len(p_data) == 0:
            return None

        if p_data[0] == "LED" and p_data[1] == self.binx.led_id:
            return bool(int(p_data[2]))

        return None
