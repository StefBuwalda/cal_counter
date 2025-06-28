from flask_login import UserMixin  # type: ignore
from werkzeug.security import generate_password_hash, check_password_hash
from application import db
from typing import Optional


class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(
        self, username: str, password: str, is_admin: bool = False
    ) -> None:
        super().__init__()
        self.username = username
        self.password = generate_password_hash(password=password)
        self.is_admin = is_admin

    def check_password(self, password: str) -> bool:
        return check_password_hash(pwhash=self.password, password=password)

    def change_password(self, password: str) -> None:
        self.password = generate_password_hash(password=password)


class Unit(db.Model):
    __tablename__ = "unit"
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10), unique=True, nullable=False)
    name = db.Column(db.String(50), unique=True, nullable=False)


class FoodItem(db.Model):
    __tablename__ = "food_item"
    id = db.Column(db.Integer, primary_key=True)
    barcode = db.Column(db.Integer)
    name = db.Column(db.String(150), unique=True, nullable=False)

    energy_100g = db.Column(db.Integer, nullable=False)
    protein_100g = db.Column(db.Float, nullable=False)
    carbs_100g = db.Column(db.Integer, nullable=False)
    sugar_100g = db.Column(db.Integer)
    fats_100g = db.Column(db.Integer, nullable=False)
    saturated_fats_100g = db.Column(db.Integer)

    def __init__(
        self,
        name: str,
        energy: int,
        protein: float,
        carbs: int,
        fats: int,
        sugar: Optional[int] = None,
        saturated_fats: Optional[int] = None,
        barcode: Optional[int] = None,
    ):
        self.name = name
        self.energy_100g = energy
        self.protein_100g = protein
        self.carbs_100g = carbs
        self.sugar_100g = sugar
        self.fats_100g = fats
        self.saturated_fats_100g = saturated_fats
        self.barcode = barcode

    def to_dict(self):
        return {
            "id": self.id,
            "barcode": self.barcode,
            "name": self.name,
            "energy_100g": self.energy_100g,
            "protein_100g": self.protein_100g,
            "carbs_100g": self.carbs_100g,
            "sugar_100g": self.sugar_100g,
            "fats_100g": self.fats_100g,
            "saturated_fats_100g": self.saturated_fats_100g,
        }
