from flask import Flask
from dotenv import load_dotenv

# Load environment variables.
load_dotenv()

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'