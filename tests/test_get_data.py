import pytest
from werkzeug.security import generate_password_hash
from app import create_app
from app.database import db
from app.models.user import User, Role, Token, ROLE_A, ROLE_B, ROLE_C

class UserTest:
    i = 0
    def __init__(self, roles):
        self.name = f'name_{UserTest.i}'
        self.pwd = f'pwd_{UserTest.i}'
        self.roles = roles.copy()
        UserTest.i += 1

userTestNoRoles = UserTest([])
userTestA = UserTest([ROLE_A])
userTestB = UserTest([ROLE_B])
userTestC = UserTest([ROLE_C])
userTestABC = UserTest([ROLE_A, ROLE_B, ROLE_C])

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
    # Roles are already created.
    tokens = list()

    usersTests = [userTestNoRoles, userTestA, userTestB, userTestC, userTestABC]
    for userTest in usersTests:
        client.post('/user', json={'name': userTest.name, 'password': userTest.pwd})
        for role_name in userTest.roles:
            data = {
                "user_name": userTest.name,
                "role_name": role_name
            }
            client.post('/assign-role', json=data)
        response = client.post('/login', json={'name': userTest.name, 'password': userTest.pwd})
        assert response.status_code == 200
        assert b'token' in response.data
        tokens.append(response.json.get('token'))

    return tokens

def test_login(client, create_data):
    """Test for the login route"""
    print(create_data)

