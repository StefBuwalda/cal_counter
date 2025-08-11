from flask import Blueprint, request, render_template, redirect, url_for
from flask_login import current_user, login_user
from forms import LoginForm, ChangePasswordForm
from models import User
from application.utils import default_return
from application import db

bp = Blueprint(
    "auth",
    __name__,
    template_folder="templates",
)


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return default_return()

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(password=form.password.data):
            # User found and password correct
            next_page = request.args.get("next")  # Get next page if given
            login_user(user)  # Log in the user
            return default_return(next_page=next_page)
        else:
            pass
            # invalid user
    return render_template("login.html", form=form)


@bp.route("/change_password", methods=["GET", "POST"])
def change_password():
    if not current_user.is_authenticated:
        return redirect(url_for("auth.login"))

    form = ChangePasswordForm()
    if form.validate_on_submit():
        cur_check = current_user.check_password(
            password=form.current_password.data
        )
        eq_check = form.new_password.data == form.confirm_password.data
        if cur_check and eq_check:
            current_user.change_password(form.new_password.data)
            current_user.set_pw_change(False)
            db.session.commit()
            return default_return()
    return render_template("change_password.html", form=form)
