from flask import Blueprint, request, jsonify, current_app
from ..database import db
from ..models.user import Token
from functools import wraps

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
            if current_app.config.get('DISABLE_ROLE_CHECK', False) or not len(required_roles):
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
