from flask import (
    Blueprint,
)
from application.utils import login_required

bp = Blueprint(
    "user",
    __name__,
    template_folder="templates",
)


bp.before_request(login_required)
