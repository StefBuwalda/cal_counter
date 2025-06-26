from application import db, app
from models import User

with app.app_context():
    User.query.delete()
    db.session.add(User("admin", "admin"))
    db.session.commit()
