from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    stream_with_context,
    url_for,
)
from flask_login import current_user, login_user, logout_user

from binday.binx.binx import BinActions, BinX
from binday.boards.board import Board, BoardType
from binday.boards.uno_r3 import UnoR3
from binday.server.factories.application import db
from binday.server.models.bin_day import BinDay
from binday.server.models.my_bin import MyBin

blueprint = Blueprint("main", __name__)


@blueprint.route("/", methods=["GET"])
def index():
    if not current_user.is_authenticated:
        return redirect(url_for("auth.login"))

    my_bin_objs = (
        MyBin.query.filter(MyBin.creator.has(id=current_user.id))
        .order_by("device_name")
        .all()
    )

    bin_sensor_data = {}
    prev_board = None

    for my_bin_obj in my_bin_objs:
        try:
            board = Board(device_name=my_bin_obj.device_name)

            if my_bin_obj.board_type == BoardType.UNO_R3:
                board = UnoR3(device_name=my_bin_obj.device_name)

            if prev_board != board:
                board.setup()
        except Exception as ex:
            flash(f"Bin {my_bin_obj.id} ({my_bin_obj.name}): {ex}", "warning")

            bin_sensor_data[my_bin_obj.id] = {
                "level": None,
                "led": None,
            }
        else:
            prev_board = board

            binx = BinX(my_bin_obj.name, my_bin_obj.sonar_id, my_bin_obj.led_id)
            bin_actions = BinActions(board, binx)

            bin_sensor_data[my_bin_obj.id] = {
                "level": bin_actions.get_bin_sonar(),
                "led": bin_actions.get_bin_led_status(),
            }

    return render_template(
        "index.html", my_bins=my_bin_objs, bin_sensor_data=bin_sensor_data
    )
