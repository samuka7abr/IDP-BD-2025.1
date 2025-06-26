from flask import Blueprint, request, jsonify
from services.rabbitmq_service import publish_message
from services.mongo_service import get_db
from datetime import datetime, timezone

messages_bp = Blueprint('messages', __name__)

@messages_bp.route('/messages', methods=['POST'])
def send_message():
    data = request.get_json()
    for field in ('chat_id', 'sender', 'receiver', 'text'):
        if field not in data:
            return jsonify({'error': f'{field} é obrigatório'}), 400

    data['timestamp'] = datetime.now(timezone.utc).isoformat()
    publish_message(data)
    return jsonify({'message': 'mensagem enfileirada'}), 202

@messages_bp.route('/messages/<chat_id>', methods=['GET'])
def get_history(chat_id):
    db = get_db()
    msgs = list(db.messages
                .find({'chat_id': chat_id})
                .sort('timestamp', 1))
    for m in msgs:
        m['_id'] = str(m['_id'])
    return jsonify(msgs), 200
