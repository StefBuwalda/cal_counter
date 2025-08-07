from flask import (
    Blueprint,
    redirect,
    url_for,
    render_template,
    session,
)
from flask_login import current_user
from forms import FoodItemForm, FoodLogForm
from application import db
from models import FoodItem, FoodLog

bp = Blueprint(
    "add_meal",
    __name__,
    url_prefix="/add_meal",
    template_folder="templates",
)


@bp.before_request
def login_required():
    if not current_user.is_authenticated:
        return redirect(url_for("login"))


@bp.route("/select_meal/<int:meal_type>", methods=["GET"])
def step1(meal_type: int):
    assert type(meal_type) is int
    assert 0 <= meal_type <= 3
    session["meal_type"] = meal_type
    return redirect(url_for("add_meal.step2"))


@bp.route("/get_barcode", methods=["GET"])
def step2():
    return render_template("scan_barcode.html")


@bp.route("/step3/<barcode>", methods=["GET"])
def step3(barcode: str):
    if "meal_type" not in session:
        return redirect("/")
    assert barcode.isdigit()
    item = current_user.food_items.filter_by(barcode=barcode).first()
    if item is None:
        # Does not exist, add item
        return redirect(url_for("add_meal.step3_alt1", barcode=barcode))
    else:
        session["item_id"] = item.id
        return redirect(url_for("add_meal.step4"))


@bp.route("/step3_alt1/<barcode>", methods=["GET", "POST"])
def step3_alt1(barcode: str):
    form = FoodItemForm()
    if form.validate_on_submit():
        print("[DEBUG] Valid form")
        if (
            current_user.food_items.filter_by(
                barcode=form.barcode.data
            ).first()
            is None
        ):
            assert form.name.data is not None
            assert form.energy.data is not None
            assert form.protein.data is not None
            assert form.carbs.data is not None
            assert form.fat.data is not None
            assert form.barcode.data is not None
            db.session.add(
                FoodItem(
                    name=form.name.data,
                    owner_id=current_user.id,
                    energy=form.energy.data,
                    protein=form.protein.data,
                    carbs=form.carbs.data,
                    fat=form.fat.data,
                    barcode=(
                        form.barcode.data
                        if form.barcode.data.isdigit()
                        else None
                    ),
                    saturated_fat=form.saturated_fat.data,
                    sugar=form.sugar.data,
                )
            )
            db.session.commit()
            print("[DEBUG] New item added")
        return redirect(url_for("add_meal.step3", barcode=form.barcode.data))
    print("[DEBUG] Invalid form")
    if barcode.isdigit():
        form.barcode.data = barcode
    return render_template("add_item.html", form=form)


@bp.route("/step4", methods=["GET", "POST"])
def step4():
    if "item_id" not in session:
        return redirect(url_for("add_meal.step2"))
    form = FoodLogForm()
    item = db.session.get(FoodItem, session["item_id"])

    assert item
    if form.validate_on_submit():
        assert form.amount.data
        db.session.add(
            FoodLog(
                food_item_id=item.id,
                user_id=current_user.id,
                amount=form.amount.data,
                part_of_day=session["meal_type"],
            )
        )
        db.session.commit()
        session.pop("meal_type")
        session.pop("item_id")
        return redirect("/")

    match session["meal_type"]:
        case 0:
            tod = "Breakfast"
        case 1:
            tod = "Lunch"
        case 2:
            tod = "Dinner"
        case 3:
            tod = "Snack"
        case _:
            tod = "Unknown"
    return render_template("step4.html", tod=tod, item=item, form=form)
