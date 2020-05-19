import time
from enum import Enum

import serial


class BoardType(Enum):
    UNO_R3 = "Uno R3"


class Board(object):
    def __init__(self, *args, **kwargs):
        self.device_name = kwargs.get("device_name", "/dev/ttyUSB0")
        self.baud_rate = kwargs.get("baud_rate", 9600)
        self.timeout = kwargs.get("timeout", 1)
        self.ser = None

    def setup(self) -> None:
        self.ser = serial.Serial(
            self.device_name, self.baud_rate, timeout=self.timeout,
        )
        time.sleep(2)

    def write(self, data: bytes) -> None:
        self.ser.write(data)

    def read(self) -> bytes:
        return self.ser.read()

    def readline(self) -> bytes:
        return self.ser.readline()
