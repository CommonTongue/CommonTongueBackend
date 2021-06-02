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
    post_data = request.json
    # accessToken may be expired
    email = post_data['email']
    firstName = post_data['firstName']
    lastName = post_data['lastName']
    photoUrl = post_data['photoUrl']
    users_collection.insert_one(
        {'email': email,
         'firstName': firstName,
         'lastName': lastName,
         'photoUrl': photoUrl,
         'level': 0,
         'decks': []
         })
    return 'Success', 200

# signup()
