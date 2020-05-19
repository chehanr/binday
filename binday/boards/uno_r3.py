from binday.boards.board import Board


class UnoR3(Board):
    def __repr__(self):
        return f"UnoR3 @{self.device_name}"
