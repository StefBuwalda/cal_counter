from flask_login import current_user
from flask import redirect, url_for, flash
from typing import Optional
from zoneinfo import ZoneInfo


def login_required():
    if not current_user.is_authenticated:
        return redirect(url_for("auth.login"))
    if current_user.must_change_password:
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


def is_valid_timezone(tz: str) -> bool:
    try:
        ZoneInfo(tz)
    except Exception:
        print(Exception)
        return False
    return True


def macro_arr_to_json(data: list[float]):
    assert len(data) == 4
    cal = data[0]
    pro = data[3]
    car = data[2]
    fat = data[1]
    macros = [
        {
            "name": "Calories",
            "current": cal,
            "target": 2000,
            "bar_width": 100 - abs(cal / 20 - 100),
            "bar_width_overflow": max(0, cal / 20 - 100),
            "unit": " kcal",
            "color": "bg-calories",
            "overflow_color": "bg-calories-dark",
        },
        {
            "name": "Protein",
            "current": pro,
            "target": 150,
            "bar_width": 100 - abs(pro / 1.5 - 100),
            "bar_width_overflow": max(0, pro / 1.5 - 100),
            "unit": "g",
            "color": "bg-protein",
            "overflow_color": "bg-protein-dark",
        },
        {
            "name": "Carbs",
            "current": car,
            "target": 250,
            "bar_width": 100 - abs(car / 2.5 - 100),
            "bar_width_overflow": max(0, car / 2.5 - 100),
            "unit": "g",
            "color": "bg-carbs",
            "overflow_color": "bg-carbs-dark",
        },
        {
            "name": "Fat",
            "current": fat,
            "target": 70,
            "bar_width": 100 - abs(fat / 0.7 - 100),
            "bar_width_overflow": max(0, fat / 0.7 - 100),
            "unit": "g",
            "color": "bg-fat",
            "overflow_color": "bg-fat-dark",
        },
    ]
    return macros
