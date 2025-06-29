from flask import Blueprint, redirect, url_for, render_template, flash
from flask_login import current_user
from application import db
from forms import FoodItemForm
from models import FoodItem

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


@user_bp.route("/add_food_item_manual", methods=["GET", "POST"])
def add_food_item_manual():
    form = FoodItemForm()
    for item in form:
        print(item)
    if form.validate_on_submit():
        assert form.name.data is not None
        assert form.energy.data is not None
        assert form.protein.data is not None
        assert form.carbs.data is not None
        assert form.fat.data is not None
        db.session.add(
            FoodItem(
                name=form.name.data,
                owner_id=current_user.id,
                energy=form.energy.data,
                protein=form.protein.data,
                carbs=form.carbs.data,
                fat=form.fat.data,
                barcode=form.barcode.data,
                saturated_fat=form.saturated_fat.data,
                sugar=form.sugar.data,
            )
        )
        db.session.commit()
        return redirect(url_for("user.dashboard"))
    return render_template("add_food_item_manual.html", form=form)
