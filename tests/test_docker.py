
import requests
import sys
import os

BASE_URL = 'http://127.0.0.1:5000'

# 1. Créer un utilisateur
user_data = {
    'name': 'TestUser',
    'password': 'password123'
}
response = requests.post(f'{BASE_URL}/user', json=user_data)
assert response.status_code == 200
print("User created:", response.json())

# 2. Créer les rôles ROLE_A, ROLE_B, ROLE_C
roles = ['ROLE_A', 'ROLE_B', 'ROLE_C']
for role in roles:
    response = requests.post(f'{BASE_URL}/role', json={'name': role})
    assert response.status_code == 200
    print(f"Role {role} created:", response.json())

# 3. Associer les rôles à l'utilisateur
for role in roles:
    data = {
        'user_name': 'TestUser',
        'role_name': role
    }
    response = requests.post(f'{BASE_URL}/assign-role', json=data)
    assert response.status_code == 200
    print(f"Role {role} assigned to user:", response.json())

# 4. Se connecter et récupérer le token
login_data = {'name': 'TestUser', 'password': 'password123'}
response = requests.post(f'{BASE_URL}/login', json=login_data)
assert response.status_code == 200
token = response.json().get('token')
print("Login successful, token:", token)

# 5. Remplir les tables A, B, C
tables_data = [
    {'url': '/tableA', 'data': {'data': 'entry A'}},
    {'url': '/tableB', 'data': {'data': 'entry B'}},
    {'url': '/tableC', 'data': {'data': 'entry C'}}
]

for table in tables_data:
    response = requests.post(f'{BASE_URL}{table["url"]}', headers={'token': token}, json=table['data'])
    assert response.status_code == 200
    print(f"Data inserted into {table['url']}:", response.json())

# 6. Afficher les tables A, B, C
response_a = requests.get(f'{BASE_URL}/tableA', headers={'token': token})
response_b = requests.get(f'{BASE_URL}/tableB', headers={'token': token})
response_c = requests.get(f'{BASE_URL}/tableC', headers={'token': token})

print("Table A:", response_a.json())
print("Table B:", response_b.json())
print("Table C:", response_c.json())
