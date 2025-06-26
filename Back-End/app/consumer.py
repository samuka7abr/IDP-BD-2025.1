import os
import pika
import json
from services.mongo_service import get_db

rabbit_url = os.getenv('RABBITMQ_URL')
params = pika.URLParameters(rabbit_url)
conn = pika.BlockingConnection(params)
chan = conn.channel()
chan.queue_declare(queue='messages', durable=True)

def callback(ch, method, properties, body):
    data = json.loads(body)
    print(f"Mensagem consumida: {data}")  
    db = get_db()
    db.messages.insert_one({
        'chat_id': data['chat_id'],
        'sender': data['sender'],
        'receiver': data['receiver'],
        'text': data['text'],
        'timestamp': data['timestamp']
    })
    ch.basic_ack(delivery_tag=method.delivery_tag)

chan.basic_qos(prefetch_count=1)
chan.basic_consume(queue='messages', on_message_callback=callback)

if __name__ == '__main__':
    print(' [*] Consumer aguardando mensagens. Para sair, Ctrl+C')
    chan.start_consuming()
