import db
from flask import Flask, request

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, World!'

@app.route("/media.json")
def index():
    return db.media_all()

@app.route("/media.json", methods=["POST"])
def create():
    title = request.form.get("title")
    type = request.form.get("type")
    status = request.form.get("status")
    notes = request.form.get("notes")
    cover_image = request.form.get("cover_image")
    rating = request.form.get("rating")
    return db.media_create(title, type, status, notes, cover_image, rating)