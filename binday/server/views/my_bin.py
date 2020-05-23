from datetime import datetime, timedelta

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user

from binday.binx.binx import BinActions, BinX
from binday.boards.board import Board, BoardType
from binday.boards.uno_r3 import UnoR3
from binday.server.factories.application import db
from binday.server.forms.my_bin import CreateMyBinForm, EditMyBinForm
from binday.server.models.bin_day import BinDay
from binday.server.models.bin_reading import BinReading
from binday.server.models.my_bin import MyBin
from binday.utils.bin_utils import get_bin_level, get_bin_level_perc
from binday.utils.common_utils import get_millis_time

blueprint = Blueprint("my_bin", __name__)


@blueprint.route("/bins/<int:bin_id>", methods=["GET"])
def view(bin_id):
    if not current_user.is_authenticated:
        return redirect(url_for("auth.login"))

    my_bin_obj = MyBin.query.filter_by(id=bin_id, creator=current_user).first_or_404()

    from_date_q = request.args.get("from_date")
    to_date_q = request.args.get("to_date")

    from_date = datetime.now() - timedelta(days=30)
    to_date = datetime.now()

    if from_date_q:
        try:
            from_date = datetime.strptime(from_date_q, "%Y%m%d")
        except ValueError as e:
            pass

    if to_date_q:
        try:
            to_date = datetime.strptime(to_date_q, "%Y%m%d")
        except ValueError as e:
            pass

    bin_reading_objs = (
        BinReading.query.filter(
            BinReading.my_bin == my_bin_obj,
            BinReading.date_created.between(from_date, to_date),
        )
        .order_by("date_created")
        .all()
    )

    bin_reading_data = {}

    for bin_reading_obj in bin_reading_objs:
        bin_reading_data[bin_reading_obj.id] = {
            "sonar_reading": bin_reading_obj.sonar_reading,
            "bin_level": get_bin_level(
                bin_reading_obj.my_bin.height, bin_reading_obj.sonar_reading
            ),
            "bin_level_perc": get_bin_level_perc(
                bin_reading_obj.my_bin.height, bin_reading_obj.sonar_reading
            ),
            "led_status": "true" if bin_reading_obj.led_status else "false",
            "date_created": get_millis_time(bin_reading_obj.date_created),
        }

    try:
        board = Board(device_name=my_bin_obj.device_name)

        if my_bin_obj.board_type == BoardType.UNO_R3:
            board = UnoR3(device_name=my_bin_obj.device_name)

        board.setup()
    except Exception as ex:
        flash(f"Bin {my_bin_obj.id} ({my_bin_obj.name}): {ex}", "warning")

        bin_sensor_data = {
            "sonar_reading": 0,
            "bin_level": 0,
            "bin_level_perc": 0.0,
            "led_status": False,
        }
    else:
        binx = BinX(my_bin_obj.name, my_bin_obj.sonar_id, my_bin_obj.led_id)
        bin_actions = BinActions(board, binx)

        sonar_reading = bin_actions.get_bin_sonar()
        led_status = bin_actions.get_bin_led_status()

        bin_sensor_data = {
            "sonar_reading": sonar_reading,
            "bin_level": get_bin_level(my_bin_obj.height, sonar_reading),
            "bin_level_perc": get_bin_level_perc(my_bin_obj.height, sonar_reading),
            "led_status": led_status,
        }

    return render_template(
        "/my_bin/view.html",
        my_bin=my_bin_obj,
        bin_reading_data=bin_reading_data,
        bin_sensor_data=bin_sensor_data,
        from_date=from_date,
        to_date=to_date,
    )


@blueprint.route("/bins/create", methods=["GET", "POST"])
def create():
    if not current_user.is_authenticated:
        return redirect(url_for("auth.login"))

    form = CreateMyBinForm()

    if form.validate_on_submit():
        bin_day_obj = BinDay(
            day_index=form.day_index.data, frequency=form.frequency.data,
        )

        my_bin_obj = MyBin(
            name=form.name.data,
            description=form.description.data,
            color_hex=form.color.data.hex,
            capacity=form.capacity.data,
            height=form.height.data,
            board_type=form.board_type.data,
            device_name=form.device_name.data,
            sonar_id=form.sonar_id.data,
            led_id=form.led_id.data,
            creator=current_user,
            bin_day=bin_day_obj,
        )

        db.session.add(my_bin_obj)
        db.session.commit()

        flash("Bin added!", "success")

        return redirect(url_for("main.index"))

    return render_template("/my_bin/create.html", form=form)


@blueprint.route("/bins/<int:bin_id>/edit", methods=["GET", "POST"])
def edit(bin_id):
    if not current_user.is_authenticated:
        return redirect(url_for("auth.login"))

    my_bin_obj = MyBin.query.filter_by(id=bin_id, creator=current_user).first_or_404()

    form = EditMyBinForm(obj=my_bin_obj)

    if form.validate_on_submit():
        my_bin_obj.name = form.name.data
        my_bin_obj.description = form.description.data
        my_bin_obj.color_hex = form.color.data.hex
        my_bin_obj.capacity = form.capacity.data
        my_bin_obj.height = form.height.data
        my_bin_obj.board_type = form.board_type.data
        my_bin_obj.device_name = form.device_name.data
        my_bin_obj.sonar_id = form.sonar_id.data
        my_bin_obj.led_id = form.led_id.data

        bin_day_obj = my_bin_obj.bin_day
        bin_day_obj.day_index = form.day_index.data
        bin_day_obj.frequency = form.frequency.data

        db.session.commit()

        flash(f"Bin id: {my_bin_obj.id} updated!", "success")

        return redirect(url_for("main.index"))

    return render_template("/my_bin/edit.html", form=form)
