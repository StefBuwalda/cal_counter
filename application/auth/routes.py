from flask import Blueprint, request, render_template
from flask_login import current_user, login_user
from forms import LoginForm
from models import User
from application.utils import default_return

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
