from .user import user_bp
from .table import table_a_bp, table_b_bp, table_c_bp
from .allowed import require_roles

def register_routes(app):
    app.register_blueprint(user_bp)
    app.register_blueprint(table_a_bp)
    app.register_blueprint(table_b_bp)
    app.register_blueprint(table_c_bp)