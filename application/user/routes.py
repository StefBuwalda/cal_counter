from flask import (
    Blueprint,
    redirect,
    url_for,
    render_template,
    flash,
    abort,
    session,
)
from flask_login import current_user
from application import db
from forms import FoodItemForm
from models import FoodItem, FoodLog
from datetime import datetime
from application.utils import login_required
from numpy import array
from zoneinfo import ZoneInfo

user_bp = Blueprint(
    "user",
    __name__,
    template_folder="templates",
)


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


user_bp.before_request(login_required)


@user_bp.route("/dashboard", methods=["GET"])
def dashboard():
    items = current_user.food_items.all()
    return render_template("dashboard.html", items=items)


@user_bp.route("/delete_food_item/<int:id>", methods=["POST"])
def delete_food_item(id: int):
    item = FoodItem.query.get(id)
    if item:
        if item.owner_id == current_user.id:
            db.session.delete(item)
            db.session.commit()
        else:
            flash("You do not own this food item!")
    else:
        flash("This food item does not exist")
    return redirect(url_for("user.dashboard"))


@user_bp.route("/edit_food_item/<int:id>", methods=["GET", "POST"])
def edit_food_item(id: int):
    item = FoodItem.query.get(id)
    if item:
        if item.owner_id == current_user.id:
            form = FoodItemForm()
            if form.validate_on_submit():
                item.updateFromForm(form=form)
                db.session.commit()
                return redirect(url_for("user.dashboard"))
            form.barcode.data = item.barcode
            form.name.data = item.name
            form.energy.data = item.energy_100
            form.protein.data = item.protein_100
            form.carbs.data = item.carbs_100
            form.sugar.data = item.sugar_100
            form.fat.data = item.fat_100
            form.saturated_fat.data = item.saturated_fat_100
            return render_template("edit_food_item.html", form=form)
    return redirect(url_for("user.dashboard"))


@user_bp.route("/daily_log2", methods=["GET"])
def daily_log2():
    # Get today's date according to user's timezone
    today = datetime.now(ZoneInfo(current_user.timezone)).date()

    # Save date in session
    session["selected_date"] = today.isoformat()

    # Get logs from today
    logs_today = current_user.food_logs.filter_by(
        date_=today.isoformat()
    ).all()

    # calculate macros
    macros = array((0.0, 0.0, 0.0, 0.0))
    for log in logs_today:
        macros += array(log.food_item.macros()) / 100 * log.amount
    macros = macro_arr_to_json(macros.tolist())

    # Render HTML
    return render_template(
        "daily_log2.html",
        macros=macros,
        logs=logs_today,
        today=today.strftime("%d/%m/%Y"),
        min=min,
    )


@user_bp.route("/remove_log/<int:id>", methods=["POST"])
def remove_log(id: int):
    log = db.session.get(FoodLog, id)
    # Check if log exists and if user owns log
    if log is None or log.user_id != current_user.id:
        abort(404)

    # Delete log
    db.session.delete(log)
    db.session.commit()
    return redirect(url_for("user.daily_log2"))
