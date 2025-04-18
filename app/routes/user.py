from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import check_password_hash, generate_password_hash
import secrets
from ..models.user import User, Role, Token
from ..database import db

user_bp = Blueprint('user_bp', __name__)

##############################################
#                  USER                      #
##############################################
@user_bp.route('/user', methods=['POST'])
def add_user():
    data = request.get_json()

    # Ensure that the password is provided and hashed
    if 'password' not in data:
        return jsonify({"error": "Password is required!"}), 400

    hashed_password = generate_password_hash(data['password'])

    # Create the new user with the hashed password
    new_user = User(name=data['name'], hashedPwd=hashed_password)

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

@user_bp.route('/token', methods=['GET'])
def get_all_tokens():
    tokens = db.session.query(Token).all()
    return jsonify([
        {"id": token.id, "token": token.token, "user_id": token.user_id} for token in tokens
    ])

##############################################
#                 OTHER                      #
##############################################
@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    name = data.get('name')
    pwd = data.get('password')

    # Get user from database
    user = db.session.query(User).filter_by(name=name).first()
    if not user:
        return jsonify({"error": "User not found!"}), 404

    # Check password
    if not check_password_hash(user.hashedPwd, pwd):
        return jsonify({"error": "Incorrect password"}), 401

    # Check if a token already exists for the user
    token = db.session.query(Token).filter_by(user_id=user.id).first()

    if not token:
        token = Token(
            token=secrets.token_hex(32),
            user_id=user.id,
            roles=user.roles.copy()
        )
        db.session.add(token)
        db.session.commit()

    return jsonify({
        "token": token.token
    }), 200


@user_bp.route('/assign-role', methods=['POST'])
def assign_role_to_user():
    data = request.get_json()

    # Get user and role from request
    user_name = data.get('user_name')
    role_name = data.get('role_name')

    # Fetch user and role from the database
    user = db.session.query(User).filter_by(name=user_name).first()
    role = db.session.query(Role).filter_by(name=role_name).first()

    # Check if user or role exists
    if not user:
        return jsonify({"error": f"User '{user_name}' not found!"}), 404
    if not role:
        return jsonify({"error": f"Role '{role_name}' not found!"}), 404

    # Force loading of the relationship if not already loaded
    if not hasattr(user, 'roles') or user.roles is None:
        user.roles = []

    # Check if the user already has the role
    if any(r.id == role.id for r in user.roles):
        return jsonify({"message": f"User '{user_name}' already has role '{role_name}'."}), 200

    # Assign role to user
    user.roles.append(role)
    db.session.add(user)  # Assure que l’objet est bien attaché à la session
    db.session.commit()

    return jsonify({"message": f"Role '{role_name}' assigned to user '{user_name}' successfully."}), 200

