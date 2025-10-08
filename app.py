from flask import redirect, url_for, send_from_directory, render_template
from flask_login import (
    login_required,
    current_user,
)
from models import User
from application import db, app, login_manager
from application.admin.routes import admin_bp
from application.user.routes import user_bp
from application.auth.routes import bp as auth_bp
from application.add_meal.routes import bp as add_meal_bp
from typing import Optional

# Config
app.config["SECRET_KEY"] = "Stef123"

login_manager.login_view = "auth.login"  # type: ignore


@login_manager.user_loader  # type: ignore
def load_user(user_id: int):
    return db.session.get(User, user_id)


# Register blueprints
app.register_blueprint(admin_bp)
app.register_blueprint(user_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(add_meal_bp)


# @app.errorhandler(404)
# def page_not_found(e):
#    return redirect("/")


# Routes
def default_return(next_page: Optional[str] = None):
    return redirect(url_for("user.daily_log"))
    if next_page:
        return redirect(next_page)
    if current_user.is_admin:
        return redirect(url_for("admin.food_items"))
    return redirect(url_for("dashboard"))


@app.route("/")
@login_required
def index():
    return redirect(url_for("auth.login"))


@app.route("/test")
@login_required
def text():
    return render_template("newBase.html")


@app.route("/favicon.ico")
def favicon():
    return send_from_directory("static", "favicon.ico")


# Run
if __name__ == "__main__":
    # If there are no users, create admin account
    with app.app_context():
        if User.query.count() == 0:
            admin = User(username="admin", password="admin", is_admin=True)
            db.session.add(admin)
            db.session.commit()

    app.run(
        host="0.0.0.0",
        port=80,
        debug=True,
    )
