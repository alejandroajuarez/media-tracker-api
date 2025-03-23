import db
from flask import Flask, request

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, World!'

# INDEX route
# This route is used to get all media items
@app.route("/media.json")
def index():
    return db.media_all()

# POST / CREATE route
# This route is used to create a new media item
@app.route("/media.json", methods=["POST"])
def create():
    title = request.form.get("title")
    type = request.form.get("type")
    status = request.form.get("status")
    notes = request.form.get("notes")
    cover_image = request.form.get("cover_image")
    rating = request.form.get("rating")
    return db.media_create(title, type, status, notes, cover_image, rating)

# SHOW route
# This route is used to get a media item by ID
@app.route("/media/<id>.json")
def show(id):
    return db.media_find_by_id(id)

# PATCH / UPDATE route
# This route is used to update a media item by ID
@app.route("/media/<id>.json", methods=["PATCH"])
def update(id):
    # Find by ID
    media = db.media_find_by_id(id)

    # Back to regular programming
    title = request.form.get("title") or media["title"]
    type = request.form.get("type") or media["type"]
    status = request.form.get("status") or media["status"]
    notes = request.form.get("notes") or media["notes"]
    cover_image = request.form.get("cover_image") or media["cover_image"]
    rating = request.form.get("rating") or media["rating"]
    return db.media_update(id, title, type, status, notes, cover_image, rating)