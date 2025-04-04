from flask import Blueprint, request, jsonify
from ..models.user import User, Role, Token
from ..database import db

user_bp = Blueprint('user_bp', __name__)

##############################################
#                  USER                      #
##############################################

@user_bp.route('/user', methods=['POST'])
def add_user():
    data = request.get_json()
    new_user = User(name=data['name'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User added successfully!"})

@user_bp.route('/user/<int:id>', methods=['GET'])
def get_user(id):
    user = db.session.get(User, id)
    if user:
        return jsonify({"id": user.id, "name": user.name})
    else:
        return jsonify({"message": "User not found!"}), 404

@user_bp.route('/user/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.get_json()
    user = db.session.get(User, id)
    if user:
        user.name = data['name']
        db.session.commit()
        return jsonify({"message": "User updated successfully!"})
    else:
        return jsonify({"message": "User not found!"}), 404

@user_bp.route('/user/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = db.session.get(User, id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted successfully!"})
    else:
        return jsonify({"message": "User not found!"}), 404

##############################################
#                  ROLE                      #
##############################################

@user_bp.route('/role', methods=['POST'])
def add_role():
    data = request.get_json()
    new_role = Role(name=data['name'])
    db.session.add(new_role)
    db.session.commit()
    return jsonify({"message": "Role added successfully!"})

@user_bp.route('/role/<int:id>', methods=['GET'])
def get_role(id):
    role = db.session.get(Role, id)
    if role:
        return jsonify({"id": role.id, "name": role.name})
    else:
        return jsonify({"message": "Role not found!"}), 404

@user_bp.route('/role/<int:id>', methods=['PUT'])
def update_role(id):
    data = request.get_json()
    role = db.session.get(Role, id)
    if role:
        role.name = data['name']
        db.session.commit()
        return jsonify({"message": "Role updated successfully!"})
    else:
        return jsonify({"message": "Role not found!"}), 404

@user_bp.route('/role/<int:id>', methods=['DELETE'])
def delete_role(id):
    role = db.session.get(Role, id)
    if role:
        db.session.delete(role)
        db.session.commit()
        return jsonify({"message": "Role deleted successfully!"})
    else:
        return jsonify({"message": "Role not found!"}), 404

##############################################
#                 TOKEN                      #
##############################################

@user_bp.route('/token', methods=['POST'])
def add_token():
    data = request.get_json()
    new_token = Token(token=data['token'], user_id=data['user_id'])
    db.session.add(new_token)
    db.session.commit()
    return jsonify({"message": "Token added successfully!"})

@user_bp.route('/token/<int:id>', methods=['GET'])
def get_token(id):
    token = db.session.get(Token, id)
    if token:
        return jsonify({"id": token.id, "token": token.token, "user_id": token.user_id})
    else:
        return jsonify({"message": "Token not found!"}), 404

@user_bp.route('/token/<int:id>', methods=['PUT'])
def update_token(id):
    data = request.get_json()
    token = db.session.get(Token, id)
    if token:
        token.token = data['token']
        db.session.commit()
        return jsonify({"message": "Token updated successfully!"})
    else:
        return jsonify({"message": "Token not found!"}), 404

@user_bp.route('/token/<int:id>', methods=['DELETE'])
def delete_token(id):
    token = db.session.get(Token, id)
    if token:
        db.session.delete(token)
        db.session.commit()
        return jsonify({"message": "Token deleted successfully!"})
    else:
        return jsonify({"message": "Token not found!"}), 404
