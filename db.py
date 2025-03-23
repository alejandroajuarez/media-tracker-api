import sqlite3

# INDEX function
def media_all():
    conn = connect_to_db()
    rows = conn.execute(
        """
        SELECT * FROM media
        """
    ).fetchall()
    return [dict(row) for row in rows]

# CREATE function
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

# SHOW function
def media_find_by_id(id):
    conn = connect_to_db()
    row = conn.execute(
        """
        SELECT * FROM media 
        WHERE id = ?
        """,
        (id,),
    ).fetchone()
    return dict(row)

# UPDATE function
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


def connect_to_db():
    conn = sqlite3.connect("media.db")
    conn.row_factory = sqlite3.Row
    return conn

def initial_setup():
    conn = connect_to_db()
    conn.execute(
        """
        DROP TABLE IF EXISTS media;
        """
    )
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
        """)

    media_seed_data = [
        ("Rhythm of War", "Book", "Saved", "Book 4 of the Stormlight Archive", "https://www.brandonsanderson.com/wp-content/uploads/2020/08/ROW-UK-Cover.jpg", None),
        ("The Way of Kings", "Book", "Completed", "Book 1 of the Stormlight Archive", "https://www.brandonsanderson.com/wp-content/uploads/2019/10/WOK-UK-Cover.jpg", 5),
        ("Dawnshard", "Book", "In-Progress", "Novella in the Stormlight Archive", "https://www.brandonsanderson.com/wp-content/uploads/2020/10/Dawnshard-UK-Cover.jpg", 5),
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


if __name__ == "__main__":
    initial_setup()