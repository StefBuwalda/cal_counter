from flask_login import current_user
from flask import redirect, url_for, flash
from typing import Optional


def login_required():
    if not current_user.is_authenticated:
        return redirect(url_for("auth.login"))
        # if current_user.must_change_password:
        flash("You have to change your password")
        return redirect(url_for("auth.change_password"))
    return


def default_return(next_page: Optional[str] = None):
    return redirect(url_for("user.daily_log"))
    if next_page:
        return redirect(next_page)
    if current_user.is_admin:
        return redirect(url_for("admin.food_items"))
    return redirect(url_for("dashboard"))
