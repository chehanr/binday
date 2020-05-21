from binday.binx.binx import BinActions, BinX
from binday.boards.board import Board, BoardType
from binday.boards.uno_r3 import UnoR3
from binday.server.factories.application import create_application
from binday.server.models.my_bin import MyBin
from binday.utils.bin_utils import get_bin_level, get_bin_level_perc


def add_bin_reading_task():
    app = create_application()

    my_bin_objs = []
    bin_sensor_data = {}

    with app.app_context():
        my_bin_objs = MyBin.query.order_by("device_name").all()

    prev_board = None

    for my_bin_obj in my_bin_objs:
        try:
            board = Board(device_name=my_bin_obj.device_name)

            if my_bin_obj.board_type == BoardType.UNO_R3:
                board = UnoR3(device_name=my_bin_obj.device_name)

            if prev_board != board:
                board.setup()
        except Exception as ex:
            # TODO Better logging.
            print(ex)
            bin_sensor_data[my_bin_obj.id] = {
                "sonar_reading": None,
                "bin_level": None,
                "bin_level_perc": None,
                "led_status": None,
            }
        else:
            prev_board = board

            binx = BinX(my_bin_obj.name, my_bin_obj.sonar_id, my_bin_obj.led_id)
            bin_actions = BinActions(board, binx)

            sonar_reading = bin_actions.get_bin_sonar()
            led_status = bin_actions.get_bin_led_status()

            bin_sensor_data[my_bin_obj.id] = {
                "sonar_reading": sonar_reading,
                "bin_level": get_bin_level(my_bin_obj.height, sonar_reading),
                "bin_level_perc": get_bin_level_perc(my_bin_obj.height, sonar_reading),
                "led_status": led_status,
            }

    # TODO Add a bin reading record.
    print(bin_sensor_data)
