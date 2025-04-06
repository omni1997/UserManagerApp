import pytest
from werkzeug.security import generate_password_hash
from app import create_app
from app.database import db
from app.models.user import User, Role, Token

@pytest.fixture
def app():
    # Create the test application
    app = create_app()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/test.db'  # Using a temporary database for tests
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TESTING'] = True
    app.config['DISABLE_ROLE_CHECK'] = True

    with app.app_context():
        db.create_all()  # Create the tables for the test database
    yield app

    with app.app_context():
        db.drop_all()  # Drop the tables after the tests

@pytest.fixture
def client(app):
    # Create a test client to interact with the application
    return app.test_client()

@pytest.fixture
def create_data(client):
    """Fixture to create a user with a hashed password"""
    user_data = {
        'name': 'Test User',
        'password': 'password123'
    }
    response = client.post('/user', json=user_data)
    return response

def test_add_user(client):
    pass

