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
from binday.server.forms.main import UserConfigForm
from binday.server.models.bin_day import BinDay
from binday.server.models.my_bin import MyBin
from binday.server.models.user_config import UserConfig
from binday.utils.bin_utils import get_bin_level, get_bin_level_perc

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

    return render_template(
        "index.html", my_bins=my_bin_objs, bin_sensor_data=bin_sensor_data
    )


@blueprint.route("/user/settings", methods=["GET", "POST"])
def user_config():
    if not current_user.is_authenticated:
        return redirect(url_for("auth.login"))

    user_cofig_obj = UserConfig.query.filter(
        UserConfig.user.has(id=current_user.id)
    ).first()

    form = UserConfigForm(obj=user_cofig_obj)

    if form.validate_on_submit():
        if user_cofig_obj:
            user_cofig_obj.pushbullet_api_key = form.pushbullet_api_key.data
            db.session.merge(user_cofig_obj)
        else:
            new_user_config = UserConfig(user=current_user)
            new_user_config.pushbullet_api_key = form.pushbullet_api_key.data
            db.session.add(new_user_config)

        db.session.commit()

        flash(f"User settings updated!", "success")

        return redirect(url_for("main.index"))

    return render_template("user_config.html", form=form)
