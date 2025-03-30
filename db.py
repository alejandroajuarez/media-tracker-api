import sqlite3

def connect_to_db():
    conn = sqlite3.connect("media.db")
    conn.row_factory = sqlite3.Row
    return conn

# Return all media entries
def media_all():
    conn = connect_to_db()
    rows = conn.execute("SELECT * FROM media").fetchall()
    return [dict(row) for row in rows]

# Create a new media entry
def media_create(title, type, status, notes, cover_image, rating):
    conn = connect_to_db()
    row = conn.execute(
        """
        INSERT INTO media (title, type, status, notes, cover_image, rating)
        VALUES (?, ?, ?, ?, ?, ?)
        RETURNING *;
        """,
        (title, type, status, notes, cover_image, rating),
    ).fetchone()
    conn.commit()
    return dict(row)

# Find a media entry by ID
def media_find_by_id(id):
    conn = connect_to_db()
    row = conn.execute("SELECT * FROM media WHERE id = ?", (id,)).fetchone()
    return dict(row)

# Update a media entry
def media_update(id, title, type, status, notes, cover_image, rating):
    conn = connect_to_db()
    row = conn.execute(
        """
        UPDATE media
        SET title = ?, type = ?, status = ?, notes = ?, cover_image = ?, rating = ?
        WHERE id = ?
        RETURNING *;
        """,
        (title, type, status, notes, cover_image, rating, id),
    ).fetchone()
    conn.commit()
    return dict(row)

# Delete a media entry
def media_destroy_by_id(id):
    conn = connect_to_db()
    conn.execute("DELETE FROM media WHERE id = ?", (id,))
    conn.commit()
    return {"message": "Media entry deleted successfully"}

# (Optional) Initialize database with starter data
def initial_setup():
    conn = connect_to_db()
    conn.execute("DROP TABLE IF EXISTS media;")
    conn.execute(
        """
        CREATE TABLE media (
            id INTEGER PRIMARY KEY NOT NULL,
            title TEXT,
            type TEXT,
            status TEXT,
            notes TEXT,
            cover_image TEXT,
            rating INTEGER
        );
        """
    )
    media_seed_data = [
        ("Rhythm of War", "Book", "Saved", "Book 4 of the Stormlight Archive", "https://www.brandonsanderson.com/wp-content/uploads/2020/08/ROW-UK-Cover.jpg", None),
        ("The Way of Kings", "Book", "Completed", "Book 1 of the Stormlight Archive", "https://www.brandonsanderson.com/wp-content/uploads/2019/10/WOK-UK-Cover.jpg", 5),
        ("Dawnshard", "Book", "In Progress", "Novella in the Stormlight Archive", "https://www.brandonsanderson.com/wp-content/uploads/2020/10/Dawnshard-UK-Cover.jpg", 5),
    ]
    conn.executemany(
        """
        INSERT INTO media (title, type, status, notes, cover_image, rating)
        VALUES (?, ?, ?, ?, ?, ?);
        """, 
        media_seed_data
    )
    conn.commit()
    print("Media database initialized")
    conn.close()
