import unittest
import json
from main import app, db, User, Role, Token, TableA, TableB, TableC

class BasicTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        cls.client = app.test_client()
        with app.app_context():
            db.create_all()

    @classmethod
    def tearDownClass(cls):
        with app.app_context():
            db.drop_all()

    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()

    def tearDown(self):
        db.session.remove()
        self.app_context.pop()

    def test_add_user(self):
        response = self.client.post('/user', data=json.dumps({'name': 'John Doe'}), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'User added successfully!', response.data)

    def test_get_user(self):
        user = User(name='Jane Doe')
        db.session.add(user)
        db.session.commit()
        response = self.client.get(f'/user/{user.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Jane Doe', response.data)

    def test_update_user(self):
        user = User(name='Jane Doe')
        db.session.add(user)
        db.session.commit()
        response = self.client.put(f'/user/{user.id}', data=json.dumps({'name': 'Jane Smith'}), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'User updated successfully!', response.data)

    def test_delete_user(self):
        user = User(name='Jane Doe')
        db.session.add(user)
        db.session.commit()
        response = self.client.delete(f'/user/{user.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'User deleted successfully!', response.data)

    # Ajoutez des tests similaires pour Role, Token, TableA, TableB, TableC

if __name__ == "__main__":
    unittest.main()