from flask import Flask
from .database import db
from .routes import register_routes
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        from .models import User, Role, Token, TableA, TableB, TableC
        db.create_all()

    register_routes(app)
    return app
