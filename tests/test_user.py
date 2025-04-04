import pytest
from app import create_app
from app.database import db
from app.models.user import User


@pytest.fixture
def app():
    # Crée l'application de test
    app = create_app()
    app.config[
        'SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/test.db'  # Utilisation d'une base de données temporaire pour les tests
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TESTING'] = True

    with app.app_context():
        db.create_all()  # Crée les tables de la base de données pour les tests
    yield app

    with app.app_context():
        db.drop_all()  # Supprime les tables après les tests


@pytest.fixture
def client(app):
    # Crée un client de test pour interagir avec l'application
    return app.test_client()


def test_add_user(client):
    """Test pour ajouter un utilisateur"""
    response = client.post('/user', json={'name': 'John Doe'})
    assert response.status_code == 200
    assert b'User added successfully!' in response.data


def test_get_user(client):
    """Test pour récupérer un utilisateur"""
    # Ajouter un utilisateur avant d'essayer de le récupérer
    client.post('/user', json={'name': 'Jane Doe'})

    response = client.get('/user/1')
    assert response.status_code == 200
    assert b'Jane Doe' in response.data


def test_update_user(client):
    """Test pour mettre à jour un utilisateur"""
    # Ajouter un utilisateur avant de le mettre à jour
    client.post('/user', json={'name': 'Alice'})

    response = client.put('/user/1', json={'name': 'Alice Updated'})
    assert response.status_code == 200
    assert b'User updated successfully!' in response.data


def test_delete_user(client):
    """Test pour supprimer un utilisateur"""
    # Ajouter un utilisateur avant de le supprimer
    client.post('/user', json={'name': 'Bob'})

    response = client.delete('/user/1')
    assert response.status_code == 200
    assert b'User deleted successfully!' in response.data

