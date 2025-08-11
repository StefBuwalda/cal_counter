from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    FloatField,
)
from wtforms.validators import DataRequired, InputRequired, Optional


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log in")


class ChangePasswordForm(FlaskForm):
    current_password = PasswordField(
        "Current password", validators=[DataRequired()]
    )
    new_password = PasswordField("New password", validators=[DataRequired()])
    confirm_password = PasswordField(
        "Confirm new password", validators=[DataRequired()]
    )
    submit = SubmitField("Change password")


class FoodItemForm(FlaskForm):
    barcode = StringField("Barcode", validators=[Optional()])
    name = StringField("Product Name", validators=[DataRequired()])
    energy = FloatField(
        "Energy per 100g",
        validators=[InputRequired()],
        render_kw={"inputmode": "decimal"},
    )
    protein = FloatField(
        "protein per 100g",
        validators=[InputRequired()],
        render_kw={"inputmode": "decimal"},
    )
    carbs = FloatField(
        "carbs per 100g",
        validators=[InputRequired()],
        render_kw={"inputmode": "decimal"},
    )
    sugar = FloatField(
        "sugar per 100g",
        validators=[Optional()],
        render_kw={"inputmode": "decimal"},
    )
    fat = FloatField(
        "fat per 100g",
        validators=[InputRequired()],
        render_kw={"inputmode": "decimal"},
    )
    saturated_fat = FloatField(
        "saturated_fat per 100g",
        validators=[Optional()],
        render_kw={"inputmode": "decimal"},
    )
    submit = SubmitField("Add Item")


class FoodLogForm(FlaskForm):
    amount = FloatField("amount of food (g/ml)", validators=[DataRequired()])
    submit = SubmitField("Log Item")
