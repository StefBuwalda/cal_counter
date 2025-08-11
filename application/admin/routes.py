from flask import Blueprint, abort
from flask_login import current_user

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
