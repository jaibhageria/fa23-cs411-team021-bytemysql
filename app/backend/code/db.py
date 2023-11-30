#db.py
import os
import pymysql
from werkzeug.security import generate_password_hash, check_password_hash
from pymysql.cursors import DictCursor

db_user = os.environ.get('CLOUD_SQL_USERNAME')
db_password = os.environ.get('CLOUD_SQL_PASSWORD')
db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')

# Google Cloud SQL configuration for local
db_config = {
    'host': '35.225.155.122',
    'user': 'root',
    'password': 'bytemysql123',
    'database': 'BeatMetrics',
    'cursorclass': DictCursor,
    'port': 3306
}

# Helper function to create a database connection
def open_connection():
    unix_socket = '/cloudsql/{}'.format(db_connection_name)
    try:
        if os.environ.get('GAE_ENV') == 'standard':
            conn = pymysql.connect(user=db_user, password=db_password,
                                unix_socket=unix_socket, db=db_name,
                                cursorclass=pymysql.cursors.DictCursor
                                )
        else:
            conn = pymysql.connect(**db_config)
    except pymysql.MySQLError as e:
        print(e)

    return conn

# Helper function to hash passwords
def hash_password(password):
    return generate_password_hash(password, method='sha256')

def login_check(user_id, password):
    conn = open_connection()
    # Query the database to check login credentials
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM User WHERE (user_id = %s)", (user_id))
        user = cursor.fetchone()
    conn.commit()
    conn.close()
    if user and user['password'] == password:
        return True
    else:
        return False

def check_user_id(user_id):
    conn = open_connection()
    # Query the database to check if user_id already exists
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM User WHERE (user_id = %s)", (user_id))
        existing_user = cursor.fetchone()
    conn.commit()
    conn.close()
    if existing_user:
        return True
    else:
        return False
    
def add_user_with_pic(user_id, password, email, first_name, last_name, phone_number, profile_picture):
    conn = open_connection()
    # Insert new user into the database with hashed password
    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO User (user_id, password, email, first_name, last_name, phone_number, picture) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                       (user_id, password, email, first_name, last_name, phone_number, profile_picture))  
    conn.commit()
    conn.close()
    return True

def add_user(user_id, password, email, first_name, last_name, phone_number):
    try:
        conn = open_connection()
        # Insert new user into the database with hashed password
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO User (user_id, password, email, first_name, last_name, phone_number) VALUES (%s, %s, %s, %s, %s, %s)",
                        (user_id, password, email, first_name, last_name, phone_number))
        conn.commit()
        conn.close()
    except:
        return False       
    return True

def fetch_all_songs():
    conn = open_connection()
    # Query the database to get all songs with artist, mood, and genre information
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT Song.*, Artist.artist_name, Artist.nationality, Artist.genre_id as artist_genre, Genre.genre_name, Mood.mood_name
            FROM Song
            JOIN Artist ON Song.artist_id = Artist.artist_id
            JOIN Mood ON Song.mood_id = Mood.mood_id
            JOIN Genre ON Song.genre_id = Genre.genre_id
        """)
        songs = cursor.fetchall()
    conn.commit()
    conn.close()
    return songs

def get_user_info(user_id):
    conn = open_connection()
    # Query the database to get user information
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM User WHERE user_id = %s", user_id)
        user = cursor.fetchone()
    conn.commit()
    conn.close()
    return user

def fetch_all_genres():
    conn = open_connection()

    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM Genre")
        genres = cursor.fetchall()
    conn.commit()
    conn.close()
    return genres

def fetch_all_moods():
    conn = open_connection()

    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM Mood")
        moods = cursor.fetchall()
    conn.commit()
    conn.close()
    return moods

def fetch_all_artists():
    conn = open_connection()

    with conn.cursor() as cursor:
        cursor.execute("SELECT artist_id, artist_name FROM Artist")
        artists = cursor.fetchall()
    conn.commit()
    conn.close()
    return artists

def update_prefs(prefs, user_id):
    conn = open_connection()

    pref_genre = prefs['genre']
    pref_mood = prefs['mood']
    pref_artist = prefs['artist']

    with conn.cursor() as cursor:
        for genre_id in pref_genre:
            cursor.execute("INSERT INTO Pref_Genre (user_id, genre_id, genre_points) VALUES (%s, %s, %s)",
                        (user_id, genre_id, 5)
            )
        for mood_id in pref_mood:
            cursor.execute("INSERT INTO Pref_Mood (user_id, mood_id, mood_points) VALUES (%s, %s, %s)",
                        (user_id, mood_id, 5)
            )
        for artist_id in pref_genre:
            cursor.execute("INSERT INTO Pref_Artist (user_id, artist_id, artist_points) VALUES (%s, %s, %s)",
                        (user_id, artist_id, 5)
            )
    conn.commit()
    conn.close()
    return True

def get_recommendations(user_id):
    conn = open_connection()

    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT s.song_id, s.title, s.release_date, g.genre_name, m.mood_name
            FROM Song s
            JOIN (
                SELECT genre_id
                FROM (
                    SELECT genre_id, COUNT(*) AS listen_count
                    FROM Listens li
                    JOIN Song so ON li.song_id = so.song_id
                    WHERE li.listener_id = %s
                    GROUP BY genre_id
                    ORDER BY listen_count DESC
                    LIMIT 1
                ) AS most_listened_genre
            ) AS max_genre ON s.genre_id = max_genre.genre_id
            JOIN (
                SELECT mood_id
                FROM (
                    SELECT mood_id, COUNT(*) AS listen_count
                    FROM Listens li
                    JOIN Song so ON li.song_id = so.song_id
                    WHERE li.listener_id = %s
                    GROUP BY mood_id
                    ORDER BY listen_count DESC
                    LIMIT 1
                ) AS most_listened_mood
            ) AS max_mood ON s.mood_id = max_mood.mood_id
            JOIN Genre g ON s.genre_id = g.genre_id
            JOIN Mood m ON s.mood_id = m.mood_id
            LIMIT 15
        """, (user_id, user_id))
        recommended_songs = cursor.fetchall()
    conn.commit()
    conn.close()
    return recommended_songs

def get_top15():
    conn = open_connection()

    with conn.cursor() as cursor:
        cursor.execute("""SELECT s.song_id, s.title, s.release_date, g.genre_name, m.mood_name
                        FROM Song s JOIN Genre g ON (s.genre_id = g.genre_id)
                        JOIN Mood m ON (s.mood_id = m.mood_id)
                        LIMIT 15
        """)
    
        top15 = cursor.fetchall()
    conn.commit()
    conn.close()
    return top15

def get_top_artists():
    conn = open_connection()

    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT
                A.artist_name,
                COUNT(DISTINCT L.listener_id) AS user_count
            FROM
                Artist A
            LEFT JOIN
                Song S ON A.artist_id = S.artist_id
            LEFT JOIN
                Listens L ON S.song_id = L.song_id
            GROUP BY
                A.artist_name
            ORDER BY
                user_count DESC
            LIMIT 15
        """)
        top_artists = cursor.fetchall()
    conn.commit()
    conn.close()
    return top_artists

def get_all_playlists(user_id):
    conn = open_connection()

    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM Playlist WHERE creator_id=%s", (user_id))
        playlists = cursor.fetchall()
    conn.commit()
    conn.close()
    return playlists

def add_to_playlist(data):
    conn = open_connection()

    playlist_id = data['playlist_id']
    song_id = data['song_id']

    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO Playlist_Songs(playlist_id, song_id) VALUES (%s, %s)", (playlist_id, song_id))
    conn.commit()
    conn.close()
    return True



