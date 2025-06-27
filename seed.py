from application import db, app
from models import User, FoodItems

with app.app_context():
    User.query.delete()
    db.session.add(User(username="admin", password="admin", is_admin=True))
    db.session.add(User(username="user", password="user", is_admin=False))

    
    
    db.session.commit()
