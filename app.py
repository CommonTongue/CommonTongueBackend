from flask import Flask, request, Response
from os import getenv
from flask_cors import CORS
import pymongo

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})


MONGO_USERNAME = getenv('MONGO_USERNAME')
MONGO_PASSWORD = getenv('MONGO_PASSWORD')
MONGO_CLUSTER_URL = getenv('MONGO_CLUSTER_URL')
MONGO_DATABASE = getenv('MONGO_DATABASE')

client_connection = f"mongodb+srv://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_CLUSTER_URL}/{MONGO_DATABASE}?retryWrites=true&w=majority"
client = pymongo.MongoClient(client_connection)
db = client.alpha
users_collection = db.users

@app.route('/', methods=["GET", "POST"])
def generic():
    print('Test')
    return 'HELLO WORLD', 200

@app.route('/signup', methods=["POST"])
def signup():
    print(request.json)
    # users_collection.insert_one({'hi': 'wow'})
    return 'Signed Up', 200

# signup()