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

from binday.server.factories.application import db
from binday.server.forms.auth import LoginForm, RegistrationForm
from binday.server.models.user import User

blueprint = Blueprint("auth", __name__)


@blueprint.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = LoginForm()

    if form.validate_on_submit():
        user_obj = User.query.filter_by(email=form.email.data).first()

        if user_obj is None or not user_obj.check_password(form.password.data):
            flash("Invalid email or password.", "danger")

            return redirect(url_for("auth.login"))

        login_user(user_obj, remember=form.remember_me.data)

        return redirect(url_for("main.index"))

    return render_template("auth/login.html", form=form)


@blueprint.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.index"))


@blueprint.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = RegistrationForm()

    if form.validate_on_submit():
        user_obj = User(email=form.email.data)
        user_obj.set_password(form.password.data)

        db.session.add(user_obj)
        db.session.commit()

        flash("Congratulations, you are now a registered!", "success")

        return redirect(url_for("auth.login"))

    return render_template("auth/register.html", form=form)
