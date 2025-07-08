from flask_login import UserMixin  # type: ignore
from werkzeug.security import generate_password_hash, check_password_hash
from application import db
from typing import Optional
from forms import FoodItemForm
from datetime import datetime, timezone, date


class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

    food_items = db.relationship("FoodItem", lazy="dynamic", backref="user")
    food_logs = db.relationship("FoodLog", lazy="dynamic", backref="user")

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
    barcode = db.Column(db.String)
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    name = db.Column(db.String(150), nullable=False)

    energy_100 = db.Column(db.Integer, nullable=False)
    protein_100 = db.Column(db.Float, nullable=False)
    carbs_100 = db.Column(db.Float, nullable=False)
    sugar_100 = db.Column(db.Float)
    fat_100 = db.Column(db.Float, nullable=False)
    saturated_fat_100 = db.Column(db.Float)

    food_logs = db.relationship("FoodLog", backref="food_item", lazy="dynamic")

    __table_args__ = (
        db.UniqueConstraint("barcode", "owner_id", name="barcode_owner_key"),
    )

    def __init__(
        self,
        name: str,
        owner_id: int,
        energy: int,
        protein: float,
        carbs: float,
        fat: float,
        barcode: Optional[str] = None,
        sugar: Optional[float] = None,
        saturated_fat: Optional[float] = None,
    ):
        if barcode and not barcode.isdigit():
            raise ValueError("Barcode must contain only digits.")
        self.name = name
        self.owner_id = owner_id
        self.energy_100 = energy
        self.protein_100 = protein
        self.carbs_100 = carbs
        self.sugar_100 = sugar
        self.fat_100 = fat
        self.saturated_fat_100 = saturated_fat
        self.barcode = barcode

    def updateFromForm(self, form: FoodItemForm):
        self.name = form.name.data
        self.energy_100 = form.energy.data
        self.protein_100 = form.protein.data
        self.carbs_100 = form.carbs.data
        self.sugar_100 = form.sugar.data
        self.fat_100 = form.fat.data
        self.saturated_fat_100 = form.saturated_fat.data

    def to_dict(self):
        return {
            "id": self.id,
            "barcode": self.barcode,
            "name": self.name,
            "owner_id": self.owner_id,
            "energy_100": self.energy_100,
            "protein_100": self.protein_100,
            "carbs_100": self.carbs_100,
            "sugar_100": self.sugar_100,
            "fat_100": self.fat_100,
            "saturated_fat_100": self.saturated_fat_100,
        }


class FoodLog(db.Model):
    __tablename__ = "food_log"
    id = db.Column(db.Integer, primary_key=True)
    datetime_created = db.Column(
        db.DateTime, default=datetime.now(timezone.utc), nullable=False
    )
    date_ = db.Column(
        db.Date, default=datetime.now(timezone.utc).date, nullable=False
    )
    food_item_id = db.Column(
        db.Integer, db.ForeignKey("food_item.id"), nullable=False
    )
    part_of_day = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    amount = db.Column(db.Integer, nullable=False)

    def __init__(
        self,
        food_item_id: int,
        user_id: int,
        amount: int,
        part_of_day: int,
        date_: Optional[date] = None,
    ):
        super().__init__()
        self.food_item_id = food_item_id
        self.user_id = user_id
        self.amount = amount
        if date_ is not None:
            self.date_ = date_
        self.part_of_day = part_of_day
