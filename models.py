from flask_login import UserMixin  # type: ignore
from werkzeug.security import generate_password_hash, check_password_hash
from application import db


class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    def __init__(self, username: str, password: str):
        super().__init__()
        self.username = username
        self.password = generate_password_hash(password=password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(pwhash=self.password, password=password)

    def change_password(self, password: str) -> None:
        self.password = generate_password_hash(password=password)


class Units(db.Model):
    __tablename__ = "unit"
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10), unique=True, nullable=False)
    name = db.Column(db.String(50), unique=True, nullable=False)


class FoodItems(db.Model):
    __tablename__ = "food_item"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    amount = db.Column(db.Integer, nullable=False)

    unit_id = db.Column(db.Integer, db.ForeignKey("unit.id"), nullable=False)
    unit = db.relationship("Units")

    energy = db.Column(db.Float)
    protein = db.Column(db.Float)
    carbs = db.Column(db.Float)
    sugar = db.Column(db.Float)
    fats = db.Column(db.Float)
    saturated_fats = db.Column(db.Float)
