from flask import Flask, request, Response
from os import getenv
from flask_cors import CORS
import pymongo
import time
import json

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


# Either creates a new user or signs in.
@app.route('/auth', methods=["POST"])
def auth():
    body = request.json
    email = body['email']
    firstName = body['firstName']
    lastName = body['lastName']
    photoUrl = body['photoUrl']
    newUser = {'email': email,
               'firstName': firstName,
               'lastName': lastName,
               'photoUrl': photoUrl,
               'level': 0,
               'decks': [],
               'lastSeen': time.time()
               }
    # if email exists, update.
    authed_user = users_collection.find_one_and_update(
        {
            'email': email
        },
        {
            '$set': newUser
        },
        upsert=True)
    # return inserted ID to locally track user on client
    # uuid = str(authed_user['_id'])
    return 'Success', 200


@app.route('/decks', methods=["GET"])
def get_decks():
    return 'Success', 200


# Adds/removes a new deck in the specified language.
@app.route('/decks', methods=["POST"])
def add_deck():
    return 'Success', 200


# Update deck by adding new cards.
# Specify the deck to effect, and the ranked word to add/remove.
@app.route('/updatedeck', methods=["POST"])
def add_word_to_deck():
    return 'Success', 200


@app.route('/levelup', methods=["POST"])
def level_up():
    body = request.json
    email = body['email']
    users_collection.update_one(
        {
            'email': email,
        },
        {
            '$inc': {
                'level': 1
            }
        }
    )
    return 'Success', 200
# Fetch cards for exploration.
# Returns explore cards in the specified language,
# along with the specified translation language.
# Provide start-end ranks to return.


@app.route('/explore', methods=["GET"])
def explore():
    return 'Success', 200
