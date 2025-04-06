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
def create_user(client):
    """Fixture to create a user with a hashed password"""
    user_data = {
        'name': 'Test User',
        'password': 'password123'
    }
    response = client.post('/user', json=user_data)
    return response

def test_add_user(client):
    """Test for adding a user"""
    password = 'password123'  # Hash the password
    user_data = {
        'name': 'John Doe',
        'password': password  # Include the hashed password
    }
    response = client.post('/user', json=user_data)
    assert response.status_code == 200
    assert b'User added successfully!' in response.data

def test_get_user(client):
    """Test for getting a user"""
    # Add a user before trying to get it
    password = 'password123'
    client.post('/user', json={'name': 'Jane Doe', 'password': password})

    response = client.get('/user/1')
    assert response.status_code == 200
    assert b'Jane Doe' in response.data

def test_update_user(client):
    """Test for updating a user"""
    # Add a user before updating it
    password = 'password123'
    client.post('/user', json={'name': 'Alice', 'password': password})

    response = client.put('/user/1', json={'name': 'Alice Updated'})
    assert response.status_code == 200
    assert b'User updated successfully!' in response.data


def test_delete_user(client):
    """Test for deleting a user"""
    # Add a user before deleting it
    password = 'password123'
    client.post('/user', json={'name': 'Bob', 'password': password})

    response = client.delete('/user/1')
    assert response.status_code == 200
    assert b'User deleted successfully!' in response.data

def test_add_role(client):
    """Test for adding a role"""
    response = client.post('/role', json={'name': 'Admin'})
    assert response.status_code == 200
    assert b'Role added successfully!' in response.data

def test_get_role(client):
    """Test for getting a role"""
    # Add a role before trying to get it
    client.post('/role', json={'name': 'Admin'})

    response = client.get('/role/1')
    assert response.status_code == 200
    assert b'Admin' in response.data

def test_update_role(client):
    """Test for updating a role"""
    # Add a role before updating it
    client.post('/role', json={'name': 'Admin'})

    response = client.put('/role/1', json={'name': 'SuperAdmin'})
    assert response.status_code == 200
    assert b'Role updated successfully!' in response.data

def test_delete_role(client):
    """Test for deleting a role"""
    # Add a role before deleting it
    client.post('/role', json={'name': 'Admin'})

    response = client.delete('/role/1')
    assert response.status_code == 200
    assert b'Role deleted successfully!' in response.data

def test_add_token(client):
    """Test for adding a token"""
    # Create a user and add a token
    password = 'password123'
    user_response = client.post('/user', json={'name': 'Test User', 'password': password})
    user_id = 1  # Assuming the user created has ID 1
    token_data = {'token': 'sample-token', 'user_id': user_id}
    response = client.post('/token', json=token_data)
    assert response.status_code == 200
    assert b'Token added successfully!' in response.data

def test_get_token(client):
    """Test for getting a token"""
    # Create a token before trying to get it
    password = 'password123'
    user_response = client.post('/user', json={'name': 'Test User', 'password': password})
    user_id = 1  # Assuming the user created has ID 1
    client.post('/token', json={'token': 'sample-token', 'user_id': user_id})

    response = client.get('/token/1')
    assert response.status_code == 200
    assert b'sample-token' in response.data

def test_update_token(client):
    """Test for updating a token"""
    # Create a token before updating it
    password = 'password123'
    user_response = client.post('/user', json={'name': 'Test User', 'password': password})
    user_id = 1  # Assuming the user created has ID 1
    client.post('/token', json={'token': 'sample-token', 'user_id': user_id})

    response = client.put('/token/1', json={'token': 'new-sample-token'})
    assert response.status_code == 200
    assert b'Token updated successfully!' in response.data

def test_delete_token(client):
    """Test for deleting a token"""
    # Create a token before deleting it
    password = 'password123'
    user_response = client.post('/user', json={'name': 'Test User', 'password': password})
    user_id = 1  # Assuming the user created has ID 1
    client.post('/token', json={'token': 'sample-token', 'user_id': user_id})

    response = client.delete('/token/1')
    assert response.status_code == 200
    assert b'Token deleted successfully!' in response.data

def test_login(client, create_user):
    """Test for the login route"""
    # Perform login for the first time
    response = client.post('/login', json={'username': 'Test User', 'password': 'password123'})

    assert response.status_code == 200
    assert b'token' in response.data  # Ensure that the token is returned
    first_token = response.json.get('token')

    # Perform login again to check if the token is the same
    response = client.post('/login', json={'username': 'Test User', 'password': 'password123'})

    assert response.status_code == 200
    assert b'token' in response.data  # Ensure that the token is returned again
    second_token = response.json.get('token')

    # Assert that both tokens are the same
    assert first_token == second_token, "Tokens should be the same on subsequent logins"
