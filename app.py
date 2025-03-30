import db
from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app,
     origins=["http://localhost:5173"],  # exact match with frontend
     supports_credentials=True) 


# INDEX route
# This route is used to get all media items
@app.route("/media.json")
def index():
    return db.media_all()

# POST / CREATE route
# This route is used to create a new media item
@app.route("/media.json", methods=["POST"])
def create():
    data = request.get_json()  # Get JSON data from the Vue form submission

    # Extract fields from the JSON payload
    title = data.get("title")
    type = data.get("type")
    status = data.get("status")
    notes = data.get("notes")
    cover_image = data.get("cover_image")
    rating = data.get("rating")

    # ✅ Call the db function to create the record
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
    data = request.get_json()

    media = db.media_find_by_id(id)  # Existing entry

    title = data.get("title") or media["title"]
    type = data.get("type") or media["type"]
    status = data.get("status") or media["status"]
    notes = data.get("notes") or media["notes"]
    cover_image = data.get("cover_image") or media["cover_image"]
    rating = data.get("rating") or media["rating"]

    return db.media_update(id, title, type, status, notes, cover_image, rating)


# DELETE route
# This route is used to delete a media item by ID
@app.route("/media/<id>.json", methods=["DELETE"])
def delete(id):
    return db.media_destroy_by_id(id)