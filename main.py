from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

########################################################################################################################
#                                                           START APP                                                  #
########################################################################################################################

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  # Utilisation de SQLite pour la simplicité
db = SQLAlchemy(app)

########################################################################################################################
#                                                           MODELS                                                     #
########################################################################################################################

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    roles = db.relationship('Role', secondary='user_roles', backref=db.backref('users', lazy='dynamic'))
    tokens = db.relationship('Token', backref='user', lazy=True)

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(120), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

user_roles = db.Table('user_roles',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True)
)

class TableA(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(120), nullable=False)

class TableB(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(120), nullable=False)

class TableC(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(120), nullable=False)

########################################################################################################################
#                                                           INIT                                                       #
########################################################################################################################
print('[START] INIT')

with app.app_context():
    db.create_all()

print('[ END ] INIT')

########################################################################################################################
#                                                           CRUD                                                       #
########################################################################################################################
@app.route('/user', methods=['POST'])
def add_user():
    data = request.get_json()
    new_user = User(name=data['name'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User added successfully!"})

@app.route('/user/<int:id>', methods=['GET'])
def get_user(id):
    user = db.session.get(User, id)
    if user:
        return jsonify({"name": user.name})
    else:
        return jsonify({"message": "User not found!"})

@app.route('/user/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.get_json()
    user = db.session.get(User, id)
    if user:
        user.name = data['name']
        db.session.commit()
        return jsonify({"message": "User updated successfully!"})
    else:
        return jsonify({"message": "User not found!"})

@app.route('/user/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = db.session.get(User, id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted successfully!"})
    else:
        return jsonify({"message": "User not found!"})

@app.route('/role', methods=['POST'])
def add_role():
    data = request.get_json()
    new_role = Role(name=data['name'])
    db.session.add(new_role)
    db.session.commit()
    return jsonify({"message": "Role added successfully!"})

@app.route('/role/<int:id>', methods=['GET'])
def get_role(id):
    role = db.session.get(Role, id)
    if role:
        return jsonify({"name": role.name})
    else:
        return jsonify({"message": "Role not found!"})

@app.route('/role/<int:id>', methods=['PUT'])
def update_role(id):
    data = request.get_json()
    role = db.session.get(Role, id)
    if role:
        role.name = data['name']
        db.session.commit()
        return jsonify({"message": "Role updated successfully!"})
    else:
        return jsonify({"message": "Role not found!"})

@app.route('/role/<int:id>', methods=['DELETE'])
def delete_role(id):
    role = db.session.get(Role, id)
    if role:
        db.session.delete(role)
        db.session.commit()
        return jsonify({"message": "Role deleted successfully!"})
    else:
        return jsonify({"message": "Role not found!"})

@app.route('/token', methods=['POST'])
def add_token():
    data = request.get_json()
    new_token = Token(token=data['token'], user_id=data['user_id'])
    db.session.add(new_token)
    db.session.commit()
    return jsonify({"message": "Token added successfully!"})

@app.route('/token/<int:id>', methods=['GET'])
def get_token(id):
    token = db.session.get(Token, id)
    if token:
        return jsonify({"token": token.token, "user_id": token.user_id})
    else:
        return jsonify({"message": "Token not found!"})

@app.route('/token/<int:id>', methods=['PUT'])
def update_token(id):
    data = request.get_json()
    token = db.session.get(Token, id)
    if token:
        token.token = data['token']
        db.session.commit()
        return jsonify({"message": "Token updated successfully!"})
    else:
        return jsonify({"message": "Token not found!"})

@app.route('/token/<int:id>', methods=['DELETE'])
def delete_token(id):
    token = db.session.get(Token, id)
    if token:
        db.session.delete(token)
        db.session.commit()
        return jsonify({"message": "Token deleted successfully!"})
    else:
        return jsonify({"message": "Token not found!"})

@app.route('/tableA', methods=['POST'])
def add_tableA():
    data = request.get_json()
    new_entry = TableA(data=data['data'])
    db.session.add(new_entry)
    db.session.commit()
    return jsonify({"message": "Entry added to TableA successfully!"})

@app.route('/tableA/<int:id>', methods=['GET'])
def get_tableA(id):
    entry = db.session.get(TableA, id)
    if entry:
        return jsonify({"data": entry.data})
    else:
        return jsonify({"message": "Entry not found in TableA!"})

@app.route('/tableA/<int:id>', methods=['PUT'])
def update_tableA(id):
    data = request.get_json()
    entry = db.session.get(TableA, id)
    if entry:
        entry.data = data['data']
        db.session.commit()
        return jsonify({"message": "Entry in TableA updated successfully!"})
    else:
        return jsonify({"message": "Entry not found in TableA!"})

@app.route('/tableA/<int:id>', methods=['DELETE'])
def delete_tableA(id):
    entry = db.session.get(TableA, id)
    if entry:
        db.session.delete(entry)
        db.session.commit()
        return jsonify({"message": "Entry deleted from TableA successfully!"})
    else:
        return jsonify({"message": "Entry not found in TableA!"})

@app.route('/tableB', methods=['POST'])
def add_tableB():
    data = request.get_json()
    new_entry = TableB(data=data['data'])
    db.session.add(new_entry)
    db.session.commit()
    return jsonify({"message": "Entry added to TableB successfully!"})

@app.route('/tableB/<int:id>', methods=['GET'])
def get_tableB(id):
    entry = db.session.get(TableB, id)
    if entry:
        return jsonify({"data": entry.data})
    else:
        return jsonify({"message": "Entry not found in TableB!"})

@app.route('/tableB/<int:id>', methods=['PUT'])
def update_tableB(id):
    data = request.get_json()
    entry = db.session.get(TableB, id)
    if entry:
        entry.data = data['data']
        db.session.commit()
        return jsonify({"message": "Entry in TableB updated successfully!"})
    else:
        return jsonify({"message": "Entry not found in TableB!"})

@app.route('/tableB/<int:id>', methods=['DELETE'])
def delete_tableB(id):
    entry = db.session.get(TableB, id)
    if entry:
        db.session.delete(entry)
        db.session.commit()
        return jsonify({"message": "Entry deleted from TableB successfully!"})
    else:
        return jsonify({"message": "Entry not found in TableB!"})

@app.route('/tableC', methods=['POST'])
def add_tableC():
    data = request.get_json()
    new_entry = TableC(data=data['data'])
    db.session.add(new_entry)
    db.session.commit()
    return jsonify({"message": "Entry added to TableC successfully!"})

@app.route('/tableC/<int:id>', methods=['GET'])
def get_tableC(id):
    entry = db.session.get(TableC, id)
    if entry:
        return jsonify({"data": entry.data})
    else:
        return jsonify({"message": "Entry not found in TableC!"})

@app.route('/tableC/<int:id>', methods=['PUT'])
def update_tableC(id):
    data = request.get_json()
    entry = db.session.get(TableC, id)
    if entry:
        entry.data = data['data']
        db.session.commit()
        return jsonify({"message": "Entry in TableC updated successfully!"})
    else:
        return jsonify({"message": "Entry not found in TableC!"})

@app.route('/tableC/<int:id>', methods=['DELETE'])
def delete_tableC(id):
    entry = db.session.get(TableC, id)
    if entry:
        db.session.delete(entry)
        db.session.commit()
        return jsonify({"message": "Entry deleted from TableC successfully!"})
    else:
        return jsonify({"message": "Entry not found in TableC!"})

########################################################################################################################
#                                                           START                                                      #
########################################################################################################################
if __name__ == "__main__":
    print('[START] APP')
    app.run(debug=True)
    print('[ END ] APP')
