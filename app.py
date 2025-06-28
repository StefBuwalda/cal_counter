from flask import render_template, redirect, url_for
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

# Config
app.config["SECRET_KEY"] = "Iman"

login_manager.login_view = "login"  # type: ignore


@login_manager.user_loader  # type: ignore
def load_user(user_id: int):
    return db.session.get(User, user_id)


# Register blueprints
app.register_blueprint(admin_bp)


# Routes


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(password=form.password.data):
            # User found and password correct
            login_user(user)
            return redirect(url_for("dashboard"))
        else:
            pass
            # invalid user
    return render_template("login.html", form=form)


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", name=current_user.username)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


# Run

if __name__ == "__main__":
    app.run(debug=True)
