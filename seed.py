from application import db, app
from models import User, FoodItem

with app.app_context():
    User.query.delete()
    db.session.add(User(username="admin", password="admin", is_admin=True))
    db.session.add(User(username="user", password="user", is_admin=False))

    FoodItem.query.delete()
    db.session.add(
        FoodItem(
            name="AH Matcha cookie",
            energy=430,
            fats=19,
            carbs=59,
            protein=5.5,
            saturated_fats=10,
            sugar=35,
            barcode=2278012003502,
        )
    )

    db.session.commit()
