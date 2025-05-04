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
        try:
            print('Tentative de création des tables...')
            from .models import User, Role, Token, TableA, TableB, TableC
            db.create_all()
            print('Tables créées avec succès')

            # Ensure default roles exist
            print('Vérification des rôles par défaut...')
            default_roles = [ROLE_A, ROLE_B, ROLE_C]
            for role_name in default_roles:
                if not Role.query.filter_by(name=role_name).first():
                    print(f'Ajout du rôle : {role_name}')
                    db.session.add(Role(name=role_name))
            db.session.commit()
            print('Rôles ajoutés avec succès')

        except Exception as e:
            print(f"Erreur lors de la création des tables ou des rôles : {e}")
            # Optionnellement, re-raise l'exception pour arrêter l'exécution du programme
            raise e

    register_routes(app)
    return app
