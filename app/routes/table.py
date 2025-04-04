from flask import Blueprint, request, jsonify
from ..database import db
from ..models.table import TableA, TableB, TableC

def create_table_routes(model, prefix):
    bp = Blueprint(f'{prefix}_bp', __name__)

    @bp.route(f'/{prefix}', methods=['POST'])
    def add_entry():
        data = request.get_json()
        entry = model(data=data['data'])
        db.session.add(entry)
        db.session.commit()
        return jsonify({"message": f"Entry added to {prefix} successfully!"})

    @bp.route(f'/{prefix}/<int:id>', methods=['GET'])
    def get_entry(id):
        entry = db.session.get(model, id)
        if entry:
            return jsonify({"id": entry.id, "data": entry.data})
        else:
            return jsonify({"message": f"Entry not found in {prefix}!"}), 404

    @bp.route(f'/{prefix}/<int:id>', methods=['PUT'])
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
table_a_bp = create_table_routes(TableA, 'tableA')
table_b_bp = create_table_routes(TableB, 'tableB')
table_c_bp = create_table_routes(TableC, 'tableC')
