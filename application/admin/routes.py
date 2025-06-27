from flask import Blueprint, render_template, abort
from flask_login import current_user
from models import FoodItems

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
    items = FoodItems.query.all()
    return render_template("food_items.html", items=items)
