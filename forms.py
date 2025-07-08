from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    IntegerField,
    FloatField,
)
from wtforms.validators import DataRequired, InputRequired, Optional


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class FoodItemForm(FlaskForm):
    barcode = StringField("Barcode", validators=[Optional()])
    name = StringField("Product Name", validators=[DataRequired()])
    energy = IntegerField("Energy per 100g", validators=[InputRequired()])
    protein = FloatField("protein per 100g", validators=[InputRequired()])
    carbs = FloatField("carbs per 100g", validators=[InputRequired()])
    sugar = FloatField("sugar per 100g", validators=[Optional()])
    fat = FloatField("fat per 100g", validators=[InputRequired()])
    saturated_fat = FloatField("saturated_fat per 100g")
    submit = SubmitField("Add Item")


class FoodLogForm(FlaskForm):
    amount = IntegerField("amount of food (g/ml)")
    submit = SubmitField("Log Item")
