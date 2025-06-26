from flask import Blueprint, request, jsonify
from services.mongo_service import get_db

users_bp = Blueprint('users', __name__)

@users_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data.get('username') or not data.get('name'):
        return jsonify({'error': 'username e name são obrigatórios'}), 400
    db = get_db()
    if db.users.find_one({'username': data['username']}):
        return jsonify({'error': 'username já existe'}), 409
    db.users.insert_one({
        'username': data['username'],
        'name': data['name'],
        'contacts': []
    })
    return jsonify({'message': 'usuário criado com sucesso'}), 201
