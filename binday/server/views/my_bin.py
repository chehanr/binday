from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user

from binday.server.factories.application import db
from binday.server.forms.my_bin import CreateMyBinForm, EditMyBinForm
from binday.server.models.bin_day import BinDay
from binday.server.models.my_bin import MyBin

blueprint = Blueprint("my_bin", __name__)


@blueprint.route("/bins/<int:bin_id>", methods=["GET"])
def view(bin_id):
    if not current_user.is_authenticated:
        return redirect(url_for("auth.login"))

    my_bin_obj = MyBin.query.filter_by(id=bin_id, creator=current_user).first_or_404()

    return render_template("/my_bin/view.html", my_bin=my_bin_obj)


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
