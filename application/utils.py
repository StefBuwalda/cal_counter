from flask_login import current_user
from flask import redirect, url_for, flash


def login_required():
    if not current_user.is_authenticated:
        return redirect(url_for("auth.login"))
    if current_user.must_change_password:
        flash("You have to change your password")
        return redirect(url_for("auth.change_password"))
    return
