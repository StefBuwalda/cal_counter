from flask import (
    render_template,
    redirect,
    url_for,
    request,
    send_from_directory,
)
from flask_login import (
    login_required,
    logout_user,
    login_user,
    current_user,
)
from forms import LoginForm
from models import User
from application import db, app, login_manager
from application.admin.routes import admin_bp
from application.user.routes import user_bp
from application.add_meal.routes import bp as add_meal_bp
from application.auth.routes import bp as auth_bp
from typing import Optional

# Config
app.config["SECRET_KEY"] = "Stef123"

login_manager.login_view = "login"  # type: ignore


@login_manager.user_loader  # type: ignore
def load_user(user_id: int):
    return db.session.get(User, user_id)


# Register blueprints
app.register_blueprint(admin_bp)
app.register_blueprint(user_bp)
app.register_blueprint(add_meal_bp)
app.register_blueprint(auth_bp)


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
    return redirect(url_for("login"))


@app.route("/favicon.ico")
def favicon():
    return send_from_directory("static", "favicon.ico")


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return default_return()

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(password=form.password.data):
            # User found and password correct
            next_page = request.args.get("next")  # Get next page if given
            login_user(user)  # Log in the user
            return default_return(next_page=next_page)
        else:
            pass
            # invalid user
    return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


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
