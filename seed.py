from application import db, app
from models import User, FoodItem, FoodLog

with app.app_context():
    User.query.delete()
    db.session.add(User(username="admin", password="admin", is_admin=True))
    db.session.add(User(username="user", password="user", is_admin=False))

    FoodItem.query.delete()
    db.session.add(
        FoodItem(
            name="AH Matcha cookie",
            owner_id=1,
            energy=430,
            fat=19,
            carbs=59,
            protein=5.5,
            saturated_fat=10,
            sugar=35,
            barcode="2278012003502",
        )
    )

    FoodLog.query.delete()
    db.session.add(FoodLog(1, 1, 200))
    db.session.add(FoodLog(1, 1, 200))
    db.session.add(FoodLog(1, 1, 200))
    db.session.add(FoodLog(1, 1, 200))
    db.session.add(FoodLog(1, 1, 100))

    db.session.commit()
