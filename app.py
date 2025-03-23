import db
from flask import Flask, request

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, World!'

@app.route("/media.json")
def index():
    return db.media_all()