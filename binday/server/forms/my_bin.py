from flask_wtf import FlaskForm
from wtforms import FormField, IntegerField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from wtforms_components import ColorField

from binday.boards.board import BoardType
from binday.server.models.bin_day import CollectionFrequency, DayIndex


class CreateMyBinForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    description = StringField("Description")
    color = ColorField("Bin color", validators=[DataRequired()])
    capacity = IntegerField("Bin max capacity", validators=[DataRequired()])
    height = IntegerField("Bin height", validators=[DataRequired()])

    board_type = SelectField(
        "Board type",
        choices=[(choice.name, choice.value) for choice in BoardType],
        validators=[DataRequired()],
    )
    device_name = StringField(
        "Device name",
        validators=[DataRequired()],
        render_kw={"placeholder": "/dev/ttyUSB0"},
    )
    sonar_id = StringField("Sonar sensor id", validators=[DataRequired()])
    led_id = StringField("LED id", validators=[DataRequired()])

    day_index = SelectField(
        "Collection day",
        choices=[(choice.name, choice.value) for choice in DayIndex],
        validators=[DataRequired()],
    )
    frequency = SelectField(
        "Collection frequency",
        choices=[(choice.name, choice.value) for choice in CollectionFrequency],
        validators=[DataRequired()],
    )

    submit = SubmitField("Add")


class EditMyBinForm(CreateMyBinForm):
    submit = SubmitField("Update")
