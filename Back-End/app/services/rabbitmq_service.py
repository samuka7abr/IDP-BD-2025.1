import os
import pika
import json

_rabbitmq_url = os.getenv('RABBITMQ_URL')
_params = pika.URLParameters(_rabbitmq_url)
_connection = pika.BlockingConnection(_params)
_channel = _connection.channel()
_channel.queue_declare(queue='messages', durable=True)

def publish_message(payload: dict):
    body = json.dumps(payload)
    _channel.basic_publish(
        exchange='',
        routing_key='messages',
        body=body,
        properties=pika.BasicProperties(delivery_mode=2)
    )
