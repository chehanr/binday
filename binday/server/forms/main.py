from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class UserConfigForm(FlaskForm):
    pushbullet_api_key = StringField("Pushbullet API key")

    submit = SubmitField("Update")
