from flask import render_template, redirect, url_for, request, jsonify
from flask_login import (
    login_required,
    logout_user,
    login_user,
    current_user,
)
from forms import LoginForm, FoodItemForm
from models import User, FoodItem
from application import db, app, login_manager
from application.admin.routes import admin_bp
from application.user.routes import user_bp
from typing import Optional

# Config
app.config["SECRET_KEY"] = "Iman"

login_manager.login_view = "login"  # type: ignore


@login_manager.user_loader  # type: ignore
def load_user(user_id: int):
    return db.session.get(User, user_id)


# Register blueprints
app.register_blueprint(admin_bp)
app.register_blueprint(user_bp)


# Routes


def default_return(next_page: Optional[str] = None):
    return redirect(url_for("user.dashboard"))
    if next_page:
        return redirect(next_page)
    if current_user.is_admin:
        return redirect(url_for("admin.food_items"))
    return redirect(url_for("dashboard"))


@app.route("/")
@login_required
def index():
    return redirect(url_for("login"))


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


@app.route("/scan")
@login_required
def scan():
    return render_template("scan.html")


@app.route("/nutri/<int:barcode>", methods=["GET"])
@login_required
def nutri(barcode):
    food = FoodItem.query.filter_by(barcode=barcode).first()
    if food:
        return jsonify(food.to_dict())
    else:
        return jsonify({})


@app.route("/food_item/<int:barcode>", methods=["GET"])
@login_required
def food_item(barcode):
    food = FoodItem.query.filter_by(barcode=barcode).first()
    if food:
        return render_template("food_item.html", item=food)
    else:
        return render_template(
            "add_food_item.html",
            barcode=barcode,
            form=FoodItemForm(barcode=barcode),
        )


@app.route("/add_food_item", methods=["POST"])
@login_required
def add_food_item():
    form = FoodItemForm()

    if form.validate_on_submit():
        print("[DEBUG] Valid form")
        if FoodItem.query.filter_by(barcode=form.barcode.data).first() is None:
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
                    fats=form.fat.data,
                    barcode=form.barcode.data,
                    saturated_fats=form.saturated_fat.data,
                    sugar=form.sugar.data,
                )
            )
            db.session.commit()
            print("[DEBUG] New item added")
            return redirect(url_for("food_item", barcode=form.barcode.data))
    else:
        print("[DEBUG] Invalid form")
    if form.barcode.data:
        return redirect(url_for("food_item", barcode=form.barcode.data))
    else:
        return redirect(url_for("scan"))


# Run

if __name__ == "__main__":
    app.run(debug=True)
