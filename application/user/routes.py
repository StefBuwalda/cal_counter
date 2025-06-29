from flask import Blueprint, redirect, url_for, render_template, flash
from flask_login import current_user
from application import db
from forms import FoodItemForm

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


@user_bp.route("/delete_food_item/<int:barcode>", methods=["POST"])
def delete_food_item(barcode: int):
    item = current_user.food_items.filter_by(barcode=barcode).first()
    if item:
        db.session.delete(item)
        db.session.commit()
    else:
        flash(f"You do not own a food item with barcode {barcode}")
    return redirect(url_for("user.dashboard"))


fields = [
    "barcode",
    "name",
    "energy",
    "protein",
    "carbs",
    "sugar",
    "fat",
    "saturated_fat",
]


@user_bp.route("/edit_food_item/<int:barcode>", methods=["GET", "POST"])
def edit_food_item(barcode: int):
    item = current_user.food_items.filter_by(barcode=barcode).first()
    if item:
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
    else:
        return redirect(url_for("user.dashboard"))
