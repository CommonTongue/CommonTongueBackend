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
# collection of users
users_collection = db.users
# collection of decks
decks_collection = db.decks
# collection of languages
languages_collection = db.languages
# collection of rankedwords
ranked_words_collection = db.ranked_words
# collection of translations
translations_collection = db.translations


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
    # return the fetched user object stored in the database
    # Remove uuid from JSON
    if authed_user is None:
        authed_user = newUser
    else:
        authed_user.pop('_id', None)
    return authed_user, 200


# Get user when an email is sent
@app.route('/user', methods=["POST"])
def user():
    body = request.json
    email = body['email']
    got_user = users_collection.find_one(
        {
            'email': email
        },
        {
            '_id': 0,  # Exclude id
        }
    )

    return got_user, 200


# Levels up user with the given email
@app.route('/level-up', methods=["POST"])
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


# Gets a new deck in the specified language.
@app.route('/get-decks', methods=["POST"])
def get_decks():
    body = request.json
    email = body['email']
    got_user = users_collection.find_one(
        {
            'email': email
        }
    )
    return {'decks': str(got_user['decks'])}, 200


# Specify the deck to create
@app.route('/add-deck', methods=["POST"])
def add_deck():
    body = request.json
    email = body['email']
    language = body['language']
    new_deck = decks_collection.insert_one({
        "language": language,
        "words": []
    })
    new_deck_id = new_deck.inserted_id
    users_collection.find_one_and_update(
        {
            'email': email
        },
        {
            '$push': {'decks': new_deck_id}
        }
    )
    return 'Success', 200


# Specify the deck to deck
@app.route('/remove-deck', methods=["POST"])
def remove_deck():
    body = request.json
    email = body['email']
    remove = body['remove']
    # delete deck
    decks_collection.delete_one({'_id': remove})
    # delete deck from user array
    users_collection.find_one_and_update(
        {
            'email': email
        },
        {
            '$pull': {'decks': remove}
        }
    )
    return 'Success', 200


# Specify the deck to add to and the word
@ app.route('/add-to-deck', methods=["POST"])
def add_to_deck():
    body = request.json
    deck_id = body['deck_id']
    ranked_word = body['ranked_word']
    decks_collection.update_one({
        '_id': deck_id
    }, {
        '$push': ranked_word
    })
    return 'Success', 200

# Specify the deck to remove card from
@ app.route('/remove-from-deck', methods=["POST"])
def remove_from_deck():
    body = request.json
    deck_id = body['deck_id']
    ranked_word = body['ranked_word']
    decks_collection.update_one({
        '_id': deck_id
    }, {
        '$pull': { '_id': ranked_word}
    })
    return 'Success', 200

# TODO: Specify the deck to remove
# Fetch cards for exploration.
# Returns explore cards in the specified language,
# along with the specified translation language.
# Provide start-end ranks to return.


@ app.route('/explore', methods=["GET"])
def explore():
    return 'Success', 200


@ app.route('/languages', methods=["GET"])
def languages():

    return 'Success', 200
