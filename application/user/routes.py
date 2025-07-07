from flask import Blueprint, redirect, url_for, render_template, flash
from flask_login import current_user
from application import db
from forms import FoodItemForm, FoodLogForm
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


@user_bp.route("/add_food_item", methods=["POST"])
def add_food_item():
    form = FoodItemForm()

    if form.validate_on_submit():
        print("[DEBUG] Valid form")
        if FoodItem.query.filter_by(barcode=form.barcode.data).first() is None:
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
            print("[DEBUG] New item added")
            return redirect(
                url_for("user.food_item", barcode=form.barcode.data)
            )
    else:
        print("[DEBUG] Invalid form")
    if form.barcode.data:
        return redirect(url_for("user.food_item", barcode=form.barcode.data))
    else:
        return redirect(url_for("scan"))


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


@user_bp.route("/food_item/<int:barcode>", methods=["GET"])
def food_item(barcode):
    food = FoodItem.query.filter_by(barcode=barcode).first()
    if food:
        return redirect(url_for("user.log_food", item_id=food.id))
    else:
        return render_template(
            "add_food_item.html",
            barcode=barcode,
            form=FoodItemForm(barcode=barcode),
        )


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


@user_bp.route("/log_food/<int:item_id>", methods=["GET", "POST"])
def log_food(item_id):
    form = FoodLogForm()
    if item_id is not None:
        if db.session.get(FoodItem, item_id):
            if form.validate_on_submit():
                assert form.amount.data is not None
                db.session.add(
                    FoodLog(
                        item_id,
                        current_user.id,
                        form.amount.data,
                        part_of_day=0,
                    )
                )
                db.session.commit()
                return redirect(url_for("user.dashboard"))
    return render_template("log_food.html", item_id=item_id, form=form)


@user_bp.route("/overview", methods=["GET"])
def overview():
    return render_template("overview.html")


@user_bp.route("/", methods=["GET"])
def test():
    today = datetime.now(timezone.utc).date()
    logs_today = current_user.food_logs.filter_by(date_=today).all()
    logs = {0: [], 1: [], 2: [], 3: []}
    for log in logs_today:
        logs[log.part_of_day].append(log)
    print(logs)
    return render_template(
        "test.html", date=(today.strftime("%d/%m/%y")), logs=logs
    )
