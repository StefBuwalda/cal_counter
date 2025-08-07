from flask import (
    Blueprint,
    redirect,
    url_for,
    render_template,
    flash,
    session,
    jsonify,
    abort,
)
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


@user_bp.route("/add_food_item/<string:barcode>", methods=["GET", "POST"])
def add_food_item(barcode):
    form = FoodItemForm(barcode=barcode)
    print(form)

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
        print("1")
        return render_template("add_food_item.html", form=form)
    else:
        return redirect("/")


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


@user_bp.route("/food_item/<string:barcode>", methods=["GET"])
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


@user_bp.route("/log_food", methods=["GET", "POST"])
def log_food():
    form = FoodLogForm()
    item_id = session["item_id"]
    meal_type = session["meal_type"]
    if item_id is None or meal_type is None:
        return redirect("/")
    if db.session.get(FoodItem, item_id):
        if form.validate_on_submit():
            assert form.amount.data is not None
            db.session.add(
                FoodLog(
                    item_id,
                    current_user.id,
                    form.amount.data,
                    part_of_day=meal_type,
                )
            )
            db.session.commit()
            return redirect(url_for("user.dashboard"))
    return render_template("log_food.html", form=form)


@user_bp.route("/overview", methods=["GET"])
def overview():
    return render_template("overview.html")


@user_bp.route("/select_meal/<int:meal_type>", methods=["GET"])
def select_meal(meal_type: int):
    assert type(meal_type) is int
    session["meal_type"] = meal_type
    return redirect(url_for("user.scan_product"))


@user_bp.route("/select_item/<int:item_id>", methods=["GET"])
def select_item(item_id: int):
    assert type(item_id) is int
    session["item_id"] = item_id
    return redirect(url_for("user.log_food"))


@user_bp.route("/get_foodid", methods=["GET"])
def scan_product():
    return render_template("get_item.html")


@user_bp.route("/add_meal", methods=["GET"])
def add_meal():
    meal_type = session["meal_type"]
    if meal_type is None:
        return redirect("/")
    return render_template("scan.html")


@user_bp.route("/", methods=["GET"])
def daily_log():
    today = datetime.now(timezone.utc).date()
    logs_today = current_user.food_logs.filter_by(date_=today).all()
    logs = [[], [], [], []]
    for log in logs_today:
        logs[log.part_of_day].append(log)
    print(logs)
    return render_template(
        "daily_log.html", date=(today.strftime("%d/%m/%y")), logs=logs
    )


@user_bp.route("/foodId_from_barcode/<string:barcode>", methods=["GET"])
def foodId_from_barcode(barcode: str):
    # Check if barcode contains only digits
    if not barcode.isdigit():
        return abort(
            400, description="Invalid barcode: must contain only digits"
        )

    item = current_user.food_items.filter_by(barcode=barcode).first()
    if item is None:
        return redirect(url_for("user.add_food_item", barcode=barcode))
    return jsonify({"item_id": item.id})
