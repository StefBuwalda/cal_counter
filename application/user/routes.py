from flask import (
    Blueprint,
    redirect,
    url_for,
    render_template,
    flash,
    abort,
)
from flask_login import current_user
from application import db
from forms import FoodItemForm
from models import FoodItem, FoodLog
from datetime import datetime, timezone

user_bp = Blueprint(
    "user",
    __name__,
    template_folder="templates",
)


@user_bp.before_request
def login_required():
    if not current_user.is_authenticated:
        return redirect(url_for("login"))


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


@user_bp.route("/overview", methods=["GET"])
def overview():
    return render_template("overview.html")


@user_bp.route("/", methods=["GET"])
def daily_log():
    today = datetime.now(timezone.utc).date()
    logs_today = current_user.food_logs.filter_by(date_=today).all()
    logs = [[], [], [], []]
    calories: float = 0
    protein: float = 0
    carbs: float = 0
    fat: float = 0
    for log in logs_today:
        logs[log.part_of_day].append(log)
        calories += log.amount * log.food_item.energy_100 / 100
        protein += log.amount * log.food_item.protein_100 / 100
        carbs += log.amount * log.food_item.carbs_100 / 100
        fat += log.amount * log.food_item.fat_100 / 100
    return render_template(
        "daily_log.html",
        date=(today.strftime("%d/%m/%y")),
        logs=logs,
        calories=calories,
        protein=protein,
        carbs=carbs,
        fat=fat,
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
    return redirect(url_for("user.daily_log"))
