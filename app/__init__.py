from flask import Flask
from .database import db
from .routes import register_routes
from config import Config
from .models.user import ROLE_A, ROLE_B, ROLE_C

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        from .models import User, Role, Token, TableA, TableB, TableC
        db.create_all()

        # Ensure default roles exist
        default_roles = [ROLE_A, ROLE_B, ROLE_C]
        for role_name in default_roles:
            if not Role.query.filter_by(name=role_name).first():
                db.session.add(Role(name=role_name))
        db.session.commit()

    register_routes(app)
    return app
