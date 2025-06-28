from flask import Flask
from flask_login import LoginManager  # type: ignore
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)  # Init Flask app
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"


db = SQLAlchemy(app=app)  # Init SQLAlchemy
migrate = Migrate(app=app, db=db)  # Init Migration

login_manager = LoginManager(app=app)  # Init login manager
