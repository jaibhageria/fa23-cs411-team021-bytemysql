#db.py
import os
import pymysql
from werkzeug.security import generate_password_hash, check_password_hash
from pymysql.cursors import DictCursor
import random
from helper import debug, info, error

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

# Configuration for local DB, uncomment to use local DB setup
# Change username, password accordingly
# db_config = {
#     'host': 'localhost',
#     'user': 'root',
#     'password': 'password',
#     'database': 'BeatMetrics',
#     'cursorclass': DictCursor,
#     'port': 3306
# }

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
        error(f"An error occurred: {str(e)}")
        return None
    return conn

# Helper function to hash passwords
def hash_password(password):
    return generate_password_hash(password, method='sha256')

def login_check(user_id, password):
    conn = open_connection()
    if conn is None:
        return False
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT *
                FROM User
                WHERE user_id = %s
            """, (user_id,))
            user = cursor.fetchone()
    except Exception as e:
        error(f"An error occurred: {str(e)}")
        return False
    finally:
        conn.commit()
        conn.close()
    if user and user.get('password') == password:
        return True
    else:
        return False

def check_user_id(user_id):
    conn = open_connection()
    if conn is None:
        return False
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM User WHERE user_id = %s", (user_id,))
            existing_user = cursor.fetchone()
    except Exception as e:
        error(f"An error occurred: {str(e)}")
        return False
    finally:
        conn.commit()
        conn.close()
    if existing_user:
        return True
    else:
        return False
    
def add_user_with_pic(user_id, password, email, first_name, last_name, phone_number, profile_picture):
    conn = open_connection()
    if conn is None:
        return False
    try:
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO User (user_id, password, email, first_name, last_name, phone_number, picture) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                        (user_id, password, email, first_name, last_name, phone_number, profile_picture))  
    except Exception as e:
        error(f"An error occurred: {str(e)}")
        return False
    finally:
        conn.commit()
        conn.close()
    return True

def add_user(user_id, password, email, first_name, last_name, phone_number):
    conn = open_connection()
    if conn is None:
        return False
    try:
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO User (user_id, password, email, first_name, last_name, phone_number) VALUES (%s, %s, %s, %s, %s, %s)",
                        (user_id, password, email, first_name, last_name, phone_number))
    except Exception as e:
        error(f"An error occurred: {str(e)}")
        return False   
    finally:
        conn.commit()
        conn.close()    
    return True

def fetch_all_songs():
    conn = open_connection()
    if conn is None:
        return False
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT Song.*, Artist.artist_name, Artist.nationality, Artist.genre_id as artist_genre, Genre.genre_name, Mood.mood_name
                FROM Song
                JOIN Artist ON Song.artist_id = Artist.artist_id
                JOIN Mood ON Song.mood_id = Mood.mood_id
                JOIN Genre ON Song.genre_id = Genre.genre_id
            """)
            songs = cursor.fetchall()
    except Exception as e:
        error(f"An error occurred: {str(e)}")
        return False   
    finally:
        conn.commit()
        conn.close() 
    return songs

def get_user_info(user_id):
    conn = open_connection()
    if conn is None:
        return {}
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM User WHERE user_id = %s", user_id)
            user = cursor.fetchone()
    except Exception as e:
        error(f"An error occurred: {str(e)}")
        return {}
    finally:
        conn.commit()
        conn.close()
    return user

def fetch_all_genres():
    conn = open_connection()
    if conn is None:
        return {}
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM Genre")
            genres = cursor.fetchall()
    except Exception as e:
        error(f"An error occurred: {str(e)}")
        return {}
    finally:
        conn.commit()
        conn.close()
    return genres

def fetch_all_moods():
    conn = open_connection()
    if conn is None:
        return {}
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM Mood")
            moods = cursor.fetchall()
    except Exception as e:
        error(f"An error occurred: {str(e)}")
        return {}
    finally:
        conn.commit()
        conn.close()
    return moods

def fetch_all_artists():
    conn = open_connection()
    if conn is None:
        return {}
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT artist_id, artist_name FROM Artist")
            artists = cursor.fetchall()
        artists = random.sample(artists, 20)
    except Exception as e:
        error(f"An error occurred: {str(e)}")
        return {}
    finally:
        conn.commit()
        conn.close()
    return artists

def update_prefs(prefs, user_id):
    conn = open_connection()
    if conn is None:
        return False
    genre_list = prefs.get('genre', [])
    mood_list = prefs.get('mood', [])
    artist_list = prefs.get('artist', [])
    try:
        with conn.cursor() as cursor:
            for genre_id in genre_list:
                cursor.execute(
                        "INSERT INTO Pref_Genre (user_id, genre_id, genre_points) VALUES (%s, %s, 5) ON DUPLICATE KEY UPDATE genre_points = genre_points"
                        , (user_id, genre_id)
                    )
            if len(genre_list) != 0:
                cursor.execute(
                        "DELETE FROM Pref_Genre WHERE user_id = %s AND genre_id NOT IN %s"
                        , (user_id, tuple(genre_list))
                    )
            for mood_id in mood_list:
                    cursor.execute(
                        "INSERT INTO Pref_Mood (user_id, mood_id, mood_points) VALUES (%s, %s, 5) ON DUPLICATE KEY UPDATE mood_points = mood_points"
                        , (user_id, mood_id)
                    )
            if len(mood_list) != 0:
                cursor.execute(
                        "DELETE FROM Pref_Mood WHERE user_id = %s AND mood_id NOT IN %s"
                        , (user_id, tuple(mood_list))
                    )
            for artist_id in artist_list:
                    cursor.execute(
                        "INSERT INTO Pref_Artist (user_id, artist_id, artist_points) VALUES (%s, %s, 5) ON DUPLICATE KEY UPDATE artist_points = artist_points"
                        , (user_id, artist_id)
                    )
    except Exception as e:
        error(f"An error occurred: {str(e)}")
        return False
    finally:
        conn.commit()
        conn.close()
    return True

def get_recommendations(user_id, num_songs):
    conn = open_connection()
    if conn is None:
        return {}
    try:
        with conn.cursor() as cursor:
            cursor.execute("CALL GetSongRecommendations(%s, %s)", (user_id, num_songs))
            recommended_songs = cursor.fetchall()
    except Exception as e:
        error(f"An error occurred: {str(e)}")
        return {}
    finally:
        conn.commit()
        conn.close()
    return recommended_songs

def get_top15():
    conn = open_connection()
    if conn is None:
        return {}
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT s.song_id, s.title, s.release_date, g.genre_name, m.mood_name
                FROM Song s JOIN Genre g ON (s.genre_id = g.genre_id)
                JOIN Mood m ON (s.mood_id = m.mood_id)
                LIMIT 15
            """)
            top15 = cursor.fetchall()
    except Exception as e:
        error(f"An error occurred: {str(e)}")
        return {}
    finally:
        conn.commit()
        conn.close()
    return top15

def get_top_artists():
    conn = open_connection()
    if conn is None:
        return {}
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT
                    A.artist_name,
                    A.nationality,
                    G.genre_name,
                    COUNT(DISTINCT L.listener_id) AS listener_count
                FROM
                    Artist A
                LEFT JOIN
                    Song S ON A.artist_id = S.artist_id
                LEFT JOIN
                    Listens L ON S.song_id = L.song_id
                JOIN
                    Genre G on G.genre_id = A.genre_id
                GROUP BY
                    A.artist_id
                ORDER BY
                    listener_count DESC
                LIMIT 15
            """)
            top_artists = cursor.fetchall()
    except Exception as e:
        error(f"An error occurred: {str(e)}")
        return {}
    finally:
        conn.commit()
        conn.close()
    return top_artists

def create_empty_playlist(data, user_id):
    conn = open_connection()
    if conn is None:
        return False
    name = data.get('playlist_name', [])
    try:
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO Playlist (playlist_name, creator_id) VALUES (%s, %s)", (name, user_id))
    except Exception as e:
        error(f"An error occurred: {str(e)}")
        return False
    finally:
        conn.commit()
        conn.close()
    return True


def get_all_playlists(user_id):
    conn = open_connection()
    if conn is None:
        return {}
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM Playlist WHERE creator_id=%s", (user_id))
            playlists = cursor.fetchall()
    except Exception as e:
        error(f"An error occurred: {str(e)}")
        return {}
    finally:
        conn.commit()
        conn.close()
    return playlists


def add_to_playlist(data):
    conn = open_connection()
    if conn is None:
        return False, False
    playlist_id = data.get('playlist_id', None)
    song_id = data.get('song_id', None)
    if playlist_id is None or song_id is None:
        error(f"playlist_id or song_id is None")
        return False, False
    try:
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO Playlist_Songs(playlist_id, song_id) VALUES (%s, %s)", (playlist_id, song_id))
    except pymysql.MySQLError as err:
        if err.args[0] == 45000:
            error(f"An error occurred: {str(err)}")
            return False, True
        else:
            raise
    except Exception as e:
        error(f"An error occurred: {str(e)}")
        return False, False
    finally:
        conn.commit()
        conn.close()
    return True, False

def delete_from_playlist(data):
    conn = open_connection()
    if conn is None:
        return False
    playlist_id = data.get('playlist_id', [])
    song_id = data.get('song_id', [])
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM Playlist_Songs WHERE playlist_id = %s AND song_id = %s", (playlist_id, song_id))
    except Exception as e:
        error(f"An error occurred: {str(e)}")
        return False
    finally:
        conn.commit()
        conn.close()
    return True

def find_songs_by_name(song_name, number):
    conn = open_connection()
    if conn is None:
        return {}
    try:
        with conn.cursor() as cursor:
            # Search for the song by name and join with Artist, Mood, and Genre tables
            cursor.execute(
            """
                SELECT
                    Song.song_id,
                    Song.title,
                    Song.release_date,
                    Artist.artist_name,
                    Mood.mood_name,
                    Genre.genre_name
                FROM Song
                JOIN Artist ON Song.artist_id = Artist.artist_id
                JOIN Mood ON Song.mood_id = Mood.mood_id
                JOIN Genre ON Song.genre_id = Genre.genre_id
                WHERE Song.title LIKE %s
                LIMIT %s
            """, ('%' + song_name + '%', int(number)))
            # Fetch all the matching songs with artist, mood, and genre details
            matching_songs = cursor.fetchall()
    except Exception as e:
        error(f"An error occurred: {str(e)}")
        return {}
    finally:
        # Close the cursor and connection
        cursor.close()
        conn.close()
    return matching_songs

def find_songs_by_genre(genre_name, number):
    conn = open_connection()
    if conn is None:
        return {}
    try:
        with conn.cursor() as cursor:
            # Search for the song by name and join with Artist, Mood, and Genre tables
            cursor.execute(
            """
                SELECT
                    Song.song_id,
                    Song.title,
                    Song.release_date,
                    Artist.artist_name,
                    Mood.mood_name,
                    Genre.genre_name
                FROM Song
                JOIN Artist ON Song.artist_id = Artist.artist_id
                JOIN Mood ON Song.mood_id = Mood.mood_id
                JOIN Genre ON Song.genre_id = Genre.genre_id
                WHERE Genre.genre_name LIKE %s
                LIMIT %s
            """, ('%' + genre_name + '%', int(number)))
            # Fetch all the matching songs with artist, mood, and genre details
            matching_songs = cursor.fetchall()
    except Exception as e:
        error(f"An error occurred: {str(e)}")
        return {}
    finally:
        # Close the cursor and connection
        cursor.close()
        conn.close()
    return matching_songs

def find_songs_by_mood(mood_name, number):
    conn = open_connection()
    if conn is None:
        return {}
    try:
        with conn.cursor() as cursor:
            # Search for the song by name and join with Artist, Mood, and Genre tables
            cursor.execute(
            """
                SELECT
                    Song.song_id,
                    Song.title,
                    Song.release_date,
                    Artist.artist_name,
                    Mood.mood_name,
                    Genre.genre_name
                FROM Song
                JOIN Artist ON Song.artist_id = Artist.artist_id
                JOIN Mood ON Song.mood_id = Mood.mood_id
                JOIN Genre ON Song.genre_id = Genre.genre_id
                WHERE Mood.mood_name LIKE %s
                LIMIT %s
            """, ('%' + mood_name + '%', int(number)))
            # Fetch all the matching songs with artist, mood, and genre details
            matching_songs = cursor.fetchall()
    except Exception as e:
        error(f"An error occurred: {str(e)}")
        return {}
    finally:
        # Close the cursor and connection
        cursor.close()
        conn.close()
    return matching_songs

def find_songs_by_artist(artist_name, number):
    conn = open_connection()
    if conn is None:
        return {}
    try:
        with conn.cursor() as cursor:
            # Search for the song by name and join with Artist, Mood, and Genre tables
            cursor.execute(
            """
                SELECT
                    Song.song_id,
                    Song.title,
                    Song.release_date,
                    Artist.artist_name,
                    Mood.mood_name,
                    Genre.genre_name
                FROM Song
                JOIN Artist ON Song.artist_id = Artist.artist_id
                JOIN Mood ON Song.mood_id = Mood.mood_id
                JOIN Genre ON Song.genre_id = Genre.genre_id
                WHERE Artist.artist_name LIKE %s
                LIMIT %s
            """, ('%' + artist_name + '%', int(number)))
            # Fetch all the matching songs with artist, mood, and genre details
            matching_songs = cursor.fetchall()
    except Exception as e:
        error(f"An error occurred: {str(e)}")
        return {}
    finally:
        # Close the cursor and connection
        cursor.close()
        conn.close()
    return matching_songs

def fetch_random_songs():
    conn = open_connection()
    if conn is None:
        return {}
    try:
        with conn.cursor() as cursor:
            # Fetch 20 random songs with details, ensuring no repetition
            cursor.execute("""
                SELECT
                    Song.song_id,
                    Song.title,
                    Song.release_date,
                    Artist.artist_name,
                    Mood.mood_name,
                    Genre.genre_name
                FROM Song
                JOIN Artist ON Song.artist_id = Artist.artist_id
                JOIN Mood ON Song.mood_id = Mood.mood_id
                JOIN Genre ON Song.genre_id = Genre.genre_id
                ORDER BY RAND()
                LIMIT 20
            """)
            # Fetch all the random songs with details
            random_songs = cursor.fetchall()
    except Exception as e:
        error(f"An error occurred: {str(e)}")
        return {}
    finally:
        # Close the cursor and connection
        cursor.close()
        conn.close()
    return random_songs

def update_points(song_id, swipe_direction, user_id):
    conn = open_connection()
    if conn is None:
        return False
    try:
        # Determine the points to be updated based on swipe direction
        points_to_update = -2 if swipe_direction == 'left' else 2
        with conn.cursor() as cursor:
            # Fetch genre_id, mood_id, artist_id, etc., based on the song_id
            cursor.execute("""
                SELECT genre_id, mood_id, artist_id
                FROM Song
                WHERE song_id = %s
            """, (song_id,))
            song_details = cursor.fetchone()
            if not song_details:
                error(f"Song with id: {song_id} not found")
                return False
            genre_id = song_details['genre_id']
            mood_id = song_details['mood_id']
            artist_id = song_details['artist_id']
            cursor.execute("""
                INSERT INTO Pref_Genre (user_id, genre_id, genre_points)
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE genre_points = genre_points + %s
            """, (user_id, genre_id, points_to_update, points_to_update))
            # Update points for mood
            cursor.execute("""
                INSERT INTO Pref_Mood (user_id, mood_id, mood_points)
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE mood_points = mood_points + %s
            """, (user_id, mood_id, points_to_update, points_to_update))
            # Update points for artist
            cursor.execute("""
                INSERT INTO Pref_Artist (user_id, artist_id, artist_points)
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE artist_points = artist_points + %s
            """, (user_id, artist_id, points_to_update, points_to_update))
        # Commit changes to the database
        conn.commit()
    except Exception as e:
        error(f"An error occurred: {str(e)}")
        return False
    finally:
        # Close the cursor and connection
        cursor.close()
        conn.close()
    return True

def check_user_playlist(data, user_id):
    conn = open_connection()
    if conn is None:
        return {}
    playlist_id = data.get('playlist_id', None)
    if playlist_id is None:
        error(f"playlist_id is None")
        return {}
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) AS playlist_count FROM Playlist WHERE playlist_id=%s AND creator_id=%s", (playlist_id, user_id))
            res = cursor.fetchall()
    except Exception as e:
        error(f"An error occurred: {str(e)}")
        return {}
    finally:
        conn.commit()
        conn.close()
    return res

def update_premium_status(user_id, is_premium):
    conn = open_connection()
    if conn is None:
        return False
    try:
        with conn.cursor() as cursor:
            cursor.execute("UPDATE User SET premium=%s WHERE user_id=%s", (is_premium, user_id))
    except Exception as e:
        error(f"An error occurred: {str(e)}")
        return False
    finally:
        conn.commit()
        conn.close()
    return True

def get_playlist_songs(playlist_id):
    conn = open_connection()
    if conn is None:
        return {}
    try:
        with conn.cursor() as cursor:
            # Get all songs in the playlist along with their details
            cursor.execute("""
                SELECT Song.*, Artist.artist_name, Genre.genre_name, Mood.mood_name
                FROM Playlist_Songs
                JOIN Song ON Playlist_Songs.song_id = Song.song_id
                LEFT JOIN Artist ON Song.artist_id = Artist.artist_id
                LEFT JOIN Genre ON Song.genre_id = Genre.genre_id
                LEFT JOIN Mood ON Song.mood_id = Mood.mood_id
                WHERE Playlist_Songs.playlist_id = %s
            """, (playlist_id,))
            playlist_songs = cursor.fetchall()
    except Exception as e:
        error(f"An error occurred: {str(e)}")
        return {}
    finally:
        conn.commit()
        conn.close()
    return playlist_songs