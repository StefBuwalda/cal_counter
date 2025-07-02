from flask import Blueprint, render_template, abort, redirect, url_for
from flask_login import current_user
from models import FoodItem
from application import db

admin_bp = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin",
    template_folder="templates",
)


@admin_bp.before_request
def admin_required():
    if not current_user.is_admin:
        abort(403)


@admin_bp.route("/food_items", methods=["GET"])
def food_items():
    items = FoodItem.query.all()
    return render_template("food_items.html", items=items)


@admin_bp.route("/barcode_test", methods=["GET"])
def barcode_test():
    return render_template("barcode_test.html")


@admin_bp.route("/delete_food/<int:id>", methods=["POST"])
def delete_food(id):
    item = FoodItem.query.get(id)
    if item:
        if item.owner_id == current_user.id:
            db.session.delete(item)
            db.session.commit()
    return redirect(url_for("admin.food_items"))
