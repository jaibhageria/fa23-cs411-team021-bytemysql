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

