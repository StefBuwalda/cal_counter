from flask import (
    Blueprint,
    redirect,
    url_for,
    render_template,
    session,
    request,
    jsonify,
)
from flask_login import current_user
from forms import FoodItemForm, FoodLogForm
from application import db
from models import FoodItem, FoodLog
from sqlalchemy import and_, or_
from datetime import datetime
from sqlalchemy.sql.elements import BinaryExpression
from typing import cast

bp = Blueprint(
    "add_meal",
    __name__,
    url_prefix="/add_meal",
    template_folder="templates",
)


def date_present(func):
    def check_date():
        if "selected_date" not in session:
            return redirect(url_for("user.daily_log"))


def item_selected(func):
    def check_item():
        if check_item():
            if "item_id" not in session:
                return redirect(url_for("add_meal.find_item"))


@bp.before_request
def login_required():
    if not current_user.is_authenticated:
        return redirect(url_for("auth.login"))


@date_present
@bp.route("/find_item", methods=["GET"])
def find_item():
    return render_template("find_item.html")


# TODO: Switch from this to query parameters / url args
@date_present
@bp.route("/select_item/<path:input>", methods=["GET"])
def select_item(input: str):
    # Check if input is a barcode
    if input.isdigit():
        item = current_user.food_items.filter_by(barcode=input).first()

    else:
        item = current_user.food_items.filter_by(name=input).first()

    if item is None:
        # Does not exist, add item
        return redirect(url_for("add_meal.add_new_item", input=input))

    # Track item to add and continue to next step
    session["item_id"] = item.id
    return redirect(url_for("add_meal.step4"))


@date_present
@bp.route("/add_new_item/<path:input>", methods=["GET"])
def add_new_item(input: str):
    form = FoodItemForm()

    if input.isdigit():
        form.barcode.data = input
    else:
        form.name.data = input
    return render_template("add_new_item.html", form=form)


@date_present
@bp.route("/add_new_item/<path:input>", methods=["POST"])
def post_new_item(input: str):
    form = FoodItemForm()

    if form.validate_on_submit():
        # Form has valid input
        barcode = form.barcode.data
        name = form.name.data
        assert name
        assert form.energy.data is not None
        assert form.protein.data is not None
        assert form.carbs.data is not None
        assert form.fat.data is not None

        # Check if name or barcode already exists
        name_filter = cast(BinaryExpression, FoodItem.name == name)
        barcode_filter = cast(BinaryExpression, FoodItem.barcode == barcode)
        filter_exp = or_(name_filter, barcode_filter)
        item = current_user.food_items.filter(filter_exp).first()

        if item is None:
            # Item does not exist, add to DB
            barcode = (
                barcode if barcode else None
            )  # Turn empty strings into None
            db.session.add(
                FoodItem(
                    name=name,
                    owner_id=current_user.id,
                    energy=form.energy.data,
                    protein=form.protein.data,
                    carbs=form.carbs.data,
                    fat=form.fat.data,
                    barcode=barcode,
                    saturated_fat=form.saturated_fat.data,
                    sugar=form.sugar.data,
                )
            )
            db.session.commit()
            print("[DEBUG] New FoodItem Added")
            input = barcode if barcode else name  # update input
        else:
            print(f"Item exists: {item.barcode} {item.name}")

        # Item added or already present, return to step 3.
        return redirect(url_for("add_meal.select_item", input=input))
    else:
        print("[DEBUG] Form Invalid")
        return redirect(url_for("add_meal.add_new_item", input=input))


@date_present
@item_selected
@bp.route("/step4", methods=["GET", "POST"])
def step4():
    form = FoodLogForm()
    item = db.session.get(FoodItem, session["item_id"])
    if not item:
        return redirect(url_for("add_meal.find_item"))

    if form.validate_on_submit():
        assert form.amount.data
        db.session.add(
            FoodLog(
                food_item_id=item.id,
                user_id=current_user.id,
                amount=form.amount.data,
                date_=datetime.strptime(
                    session["selected_date"], "%Y-%m-%d"
                ).date(),
            )
        )
        db.session.commit()
        session.pop("item_id")
        session.pop("selected_date")
        return redirect(url_for("user.daily_log"))

    return render_template("step4.html", item=item, form=form)


@date_present
@bp.route("/query", methods=["GET"])
def query():
    q = request.args.get("q", "").strip().lower()
    if not q:
        return jsonify([])

    words = q.split()
    filters = [
        FoodItem.name.ilike(f"%{word}%") for word in words  # type: ignore
    ]

    results = current_user.food_items.filter(and_(*filters)).all()
    return jsonify([item.name for item in results])
