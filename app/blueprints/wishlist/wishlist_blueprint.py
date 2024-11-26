from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from app.services.wishlist_service import get_all_items, add_item, delete_item
import json 

wishlist_bp = Blueprint('wishlist', __name__)

@wishlist_bp.route('/wishlist', methods=['GET'])
def get_wishlist():
    try:
        usuario = session ['usuario'] 
        items = get_all_items(usuario['id'])
        return jsonify(items), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@wishlist_bp.route('/wishlist', methods=['POST'])
def add_to_wishlist():
    data = request.json
    item_name = data.get('item_name')
    description = data.get('description', '')

    if not item_name:
        return jsonify({"error": "El campo 'item_name' es obligatorio"}), 400

    try:
        item_id = add_item(item_name, description)
        return jsonify({"message": "Elemento agregado exitosamente", "id": item_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@wishlist_bp.route('/wishlist/<int:item_id>', methods=['DELETE'])
def delete_from_wishlist(item_id):
    try:
        rows_deleted = delete_item(item_id)
        if rows_deleted == 0:
            return jsonify({"error": "Elemento no encontrado"}), 404

        return jsonify({"message": "Elemento eliminado exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500