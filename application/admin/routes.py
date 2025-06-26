from flask import Blueprint, render_template

admin_bp = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin",
    template_folder="templates",
)


@admin_bp.route("/food_items", methods=["GET"])
def food_items():
    return render_template("food_items.html")
