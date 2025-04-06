from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import check_password_hash, generate_password_hash
import secrets
from functools import wraps
from ..models.user import User, Role, Token
from ..database import db

user_bp = Blueprint('user_bp', __name__)

##############################################
#              Identification                #
##############################################
def union_with_check(list1, list2):
    for item in list1:
        if item in list2:
            return True
    return False

def get_current_token():
    token = request.headers.get("token")
    if not token:
        return None
    return token

def require_roles(*required_roles):
    def wrapper(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if current_app.config.get('DISABLE_ROLE_CHECK', False):
                return f(*args, **kwargs)

            token_value = get_current_token()
            if not token_value:
                return jsonify({"error": "Unauthorized"}), 401

            token = db.session.get(Token, token_value)
            if not union_with_check(token.roles, required_roles):
                return jsonify({"error": "Forbidden"}), 403

            return f(*args, **kwargs)
        return decorated_function
    return wrapper

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

##############################################
#                 OTHER                      #
##############################################
@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    username = data.get('username')
    pwd = data.get('password')

    # Get user from database
    user = db.session.query(User).filter_by(name=username).first()
    if not user:
        return jsonify({"error": "User not found!"}), 404  # User not found

    # Check if the password matches the stored hash
    if not check_password_hash(user.hashedPwd, pwd):
        return jsonify({"error": "Incorrect password"}), 401  # Incorrect password

    # Check if a token already exists for the user
    token = db.session.query(Token).filter_by(user_id=user.id).first()
    roles = [role.name for role in user.roles]

    if not token:
        # Create a new token if it does not exist
        new_token = Token(
            token=secrets.token_hex(32),
            user_id=user.id,
            roles = roles
        )
        db.session.add(new_token)
        db.session.commit()
        token = new_token

    return jsonify({
        "token": token.token  # Retourner uniquement le token
    })