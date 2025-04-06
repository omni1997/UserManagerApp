from flask import Blueprint, request, jsonify
from ..database import db
from ..models.table import TableA, TableB, TableC
from .allowed import require_roles
from ..models.user import ROLE_A, ROLE_B, ROLE_C

def create_table_routes(model, prefix, roles_required):
    bp = Blueprint(f'{prefix}_bp', __name__)

    @bp.route(f'/{prefix}', methods=['POST'])
    @require_roles(roles_required)
    def add_entry():
        data = request.get_json()
        entry = model(data=data['data'])
        db.session.add(entry)
        db.session.commit()
        return jsonify({"message": f"Entry added to {prefix} successfully!"})

    @bp.route(f'/{prefix}/<int:id>', methods=['GET'])
    @require_roles(roles_required)
    def get_entry(id):
        entry = db.session.get(model, id)
        if entry:
            return jsonify({"id": entry.id, "data": entry.data})
        else:
            return jsonify({"message": f"Entry not found in {prefix}!"}), 404

    @bp.route(f'/{prefix}/<int:id>', methods=['PUT'])
    @require_roles(roles_required)
    def update_entry(id):
        data = request.get_json()
        entry = db.session.get(model, id)
        if entry:
            entry.data = data['data']
            db.session.commit()
            return jsonify({"message": f"Entry in {prefix} updated successfully!"})
        else:
            return jsonify({"message": f"Entry not found in {prefix}!"}), 404

    @bp.route(f'/{prefix}/<int:id>', methods=['DELETE'])
    @require_roles(roles_required)
    def delete_entry(id):
        entry = db.session.get(model, id)
        if entry:
            db.session.delete(entry)
            db.session.commit()
            return jsonify({"message": f"Entry deleted from {prefix} successfully!"})
        else:
            return jsonify({"message": f"Entry not found in {prefix}!"}), 404

    return bp

# Instanciation des Blueprints
table_a_bp = create_table_routes(TableA, 'tableA', [])
table_b_bp = create_table_routes(TableB, 'tableB', [ROLE_B])
table_c_bp = create_table_routes(TableC, 'tableC', [ROLE_A, ROLE_C])
