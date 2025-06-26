from flask import Flask, jsonify
from dotenv import load_dotenv
import os
from pymongo import MongoClient

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')

mongo_uri = os.getenv('MONGO_URI')
mongo_client = MongoClient(mongo_uri)
db = mongo_client.get_default_database()

@app.route('/')
def index():
    return jsonify({
        'status': 'OK',
        'mongo_connected': 'users' in db.list_collection_names()
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
