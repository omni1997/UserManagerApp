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
    app.config['DISABLE_ROLE_CHECK'] = False

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
    """Fixture to create users, assign roles, log them in, and insert initial table entries"""
    tokens = []

    usersTests = [userTestNoRoles, userTestA, userTestB, userTestC, userTestABC]
    for userTest in usersTests:
        # Create user
        client.post('/user', json={'name': userTest.name, 'password': userTest.pwd})

        # Assign roles
        for role_name in userTest.roles:
            data = {
                "user_name": userTest.name,
                "role_name": role_name
            }
            client.post('/assign-role', json=data)

        # Login and get token
        response = client.post('/login', json={'name': userTest.name, 'password': userTest.pwd})
        assert response.status_code == 200
        assert b'token' in response.data
        tokens.append(response.json.get('token'))

    # Get all tokens and print each token
    response = client.get('/token', headers={"token": tokens[-1]})
    assert response.status_code == 200

    token = tokens[-1]  # Last user has all roles (ROLE_A, ROLE_B, ROLE_C)

    # Insert one entry into each table using the most privileged token
    client.post('/tableA', headers={"token": token}, json={"data": "entry A"})
    client.post('/tableB', headers={"token": token}, json={"data": "entry B"})
    client.post('/tableC', headers={"token": token}, json={"data": "entry C"})

    return tokens

def test(client, create_data):
    pass

def test_get_table_validate(client, create_data):
    """Test for the login route"""
    token_void, token_a, token_b, token_c, token_abc = create_data

    response = client.get("/tableA/1", headers={"token": token_void})
    assert response.status_code == 200
    assert response.json["id"] == 1

    response = client.get("/tableB/1", headers={"token": token_b})
    assert response.status_code == 200
    assert response.json["id"] == 1

    response = client.get("/tableC/1", headers={"token": token_c})
    assert response.status_code == 200
    assert response.json["id"] == 1

    response = client.get("/tableC/1", headers={"token": token_abc})
    assert response.status_code == 200
    assert response.json["id"] == 1


def test_get_table_forbidden(client, create_data):
    """Test that users without proper roles cannot access restricted tables"""
    token_void, token_a, token_b, token_c, token_abc = create_data

    # TableB requires ROLE_B → should fail with token_void, token_a, token_c
    for token in [token_void, token_a, token_c]:
        response = client.get("/tableB/1", headers={"token": token})
        assert response.status_code == 403

    # TableC requires ROLE_A or ROLE_C → should fail with token_void, token_b
    for token in [token_void, token_b]:
        response = client.get("/tableC/1", headers={"token": token})
        assert response.status_code == 403
        assert "error" in response.json
