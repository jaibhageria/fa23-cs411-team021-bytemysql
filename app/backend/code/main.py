#main.py
from flask import Flask, jsonify, request, session, send_file
from db import *
from helper import *
from flask_cors import CORS
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Change this to a secure secret key
app.config['SESSION_COOKIE_SAMESITE'] = None
CORS(app, supports_credentials=True)

# Define the path to the folder containing images
image_folder = os.path.join(os.getcwd(), 'images')

@app.route('/', methods=['GET'])
def home():
    return 'Welcome to BeatMetrics'

@app.route('/top_songs', methods=['GET'])
def top_songs():
    songs = []
    songs = get_top15()
    return jsonify({'songs': songs}), 200

@app.route('/top_artists', methods=['GET'])
def top_artists():
    top_artists = []
    top_artists = get_top_artists()
    return jsonify({'artists': top_artists}), 200

@app.route('/recommendations', methods=['GET'])
def recommendations():
    if 'user_id' not in session:
        return jsonify({'message': 'User not logged in'}), 401
    songs = []
    songs = get_recommendations(session.get('user_id'))
    return jsonify({'songs': songs}), 200

# API endpoint to login
@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        if not request.is_json:
            return jsonify({"msg": "Missing JSON in request"}), 400

    data = request.json
    user_id = data.get('user_id')
    password = data.get('password')

    if login_check(user_id, password):
        session['user_id'] = user_id
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401
    
# API endpoint to logout
@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return jsonify({'message': 'Logout successful'}), 200
    
# API endpoint to register
@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        if not request.is_json:
            return jsonify({"msg": "Missing JSON in request"}), 400
    
    data = request.json
    # Check if user id or email already exists
    if check_user_id(data.get('user_id')):
        return jsonify({'message': 'User id or email already exists'}), 400

    if add_user_with_pic(data['user_id'], data['password'], data['email'], data['first_name'], data['last_name'], data['phone_number'], fetch_random_user_image()):
        return jsonify({'message': 'Registration successful'}), 201
    else:
        return jsonify({"msg": "Error in API request"}), 400

# API endpoint to get user information
@app.route('/user_info', methods=['GET'])
def userinfo():
    if 'user_id' not in session:
        return jsonify({'message': 'User not logged in'}), 401

    user_id = session.get('user_id')
    user = get_user_info(user_id)
    if user:
        user['picture'] = base64_encode_picture(user['picture'])
        return jsonify(user), 200
    else:
        return jsonify({'message': 'User not found'}), 404

# API endpoint to get all songs
@app.route('/songs', methods=['GET'])
def get_songs():
    if 'user_id' not in session:
        return jsonify({'message': 'User not logged in'}), 401

    songs = fetch_all_songs()

    formatted_songs = []
    for song in songs:
        formatted_song = {
            "song_id": song["song_id"],
            "title": song["title"],
            "release_date": song["release_date"].strftime("%a, %d %b %Y %H:%M:%S GMT"),
            "artist": {
                "id": song["artist_id"],
                "artist_name": song["artist_name"],
                "nationality": song["nationality"],
                "primary_genre": song["artist_genre"],
            },
            "genre": {
                "id": song["genre_id"],
                "genre_name": song["genre_name"]
            },
            "mood": {
                "id": song["mood_id"],
                "mood_name": song["mood_name"]
            }
        }
        formatted_songs.append(formatted_song)

    return jsonify(formatted_songs), 200

# send all genres, moods and artist names and recieve the preferred selections from user
@app.route("/fetch_options", methods=['GET'])
def get_all_options():
    if 'user_id' not in session:
        return jsonify({'message': 'User not logged in'}), 401
    
    # backend sends the list of all genres, moods and artists to frontend
    if request.method == 'GET':
        genres = fetch_all_genres()
        moods = fetch_all_moods()
        artists = fetch_all_artists()

        results = {
            "genre": genres,
            "mood": moods,
            "artists": artists
        }

        return jsonify(results), 200

# send all genres, moods and artist names and recieve the preferred selections from user
@app.route("/set_preference", methods=['POST'])
def set_prefs():
    if 'user_id' not in session:
        return jsonify({'message': 'User not logged in'}), 401

    # recieve the preference selections and update the preference points for that user
    if request.method == 'POST':
        if not request.is_json:
            return jsonify({"msg": "Missing JSON in request"}), 400
        
    data = request.json  #format expected: {"genre": [genre_id1, genre_id2, ...], "artist": [artist_id1, artist_id2, ...], "mood": [mood_id1, mood_id2, ...]}
    ret = update_prefs(data, session.get("user_id"))

    if ret:
        return jsonify({"message": "preference update successful"}), 200
    else:
        return jsonify({'message': 'there was an error while updating preferences'}), 500

# display the playlists of the current user
@app.route("/playlist", methods=['GET'])
def get_playlists():
    if 'user_id' not in session:
        return jsonify({'message': 'User not logged in'}), 401

    user_id = session.get('user_id')

    if request.method == 'GET':
        playlists = get_all_playlists(user_id)
        return jsonify(playlists), 200
    

# add a new song to a playlist
@app.route("/add_song", methods=['POST'])
def add_song_to_playlist():
    if 'user_id' not in session:
        return jsonify({'message': 'User not logged in'}), 401
    user_id = session.get('user_id')
    if request.method == 'POST':
        if not request.is_json:
            return jsonify({"msg": "Missing JSON in request"}), 400
    
    data = request.json  #format expected: {"playlist_id": id, "song_id": id}

    res = jsonify(check_user_playlist(data, user_id))
    if res.get('playlist_count') < 1:
        return jsonify({"msg": f"user_id:{user_id} does not own the playlist with playlist_id:{data.get('playlist_id', None)}"}), 400

    status, limit = add_to_playlist(data)

    if status:
        return jsonify({'message': 'succesfully added song to playlist'}), 200
    elif limit:
        return jsonify({'message': 'song could not be added to playlist because max capacity has been reached'}), 200
    else:
        return jsonify({'message': 'song could not be added to playlist'}), 500

# delete a song from a playlist
@app.route("/delete_song", methods=['POST'])
def delete_song_from_playlist():
    if 'user_id' not in session:
        return jsonify({'message': 'User not logged in'}), 401
    
    if request.method == 'POST':
        if not request.is_json:
            return jsonify({"msg": "Missing JSON in request"}), 400
    
    data = request.json #format expected: {"playlist_id": id, "song_id": id}
    if delete_from_playlist(data):
        return jsonify({'message': 'succesfully deleted song from playlist'}), 200
    else:
        return jsonify({'message': 'song could not be deleted from playlist'}), 500

# create new empty playlist
@app.route("/create_playlist", methods=['POST'])
def create_playlist():
    if 'user_id' not in session:
        return jsonify({'message': 'User not logged in'}), 401
    
    if request.method == 'POST':
        if not request.is_json:
            return jsonify({"msg": "Missing JSON in request"}), 400
    
    data = request.json  #format expected: {'playlist_name' : name}
    user_id = session.get('user_id')
    
    if create_empty_playlist(data, user_id):
        return jsonify({'message': 'succesfully created playlist'}), 200
    else:
        return jsonify({'error': 'playlist could not be created'}), 500
    
# API endpoint to search for a song by name
@app.route('/search_song', methods=['GET'])
def search_songs():
    if 'user_id' not in session:
        return jsonify({'error': 'User not logged in'}), 401
    # Get the song name from the query parameters
    song_name = request.args.get('song_name')
    filter_type = request.args.get('filter')
    # Validate if 'song_name' is present in the query parameters
    if song_name is None:
        return jsonify({'error': 'Song name is missing in the request.'}), 400
    try:
        results = find_songs_by_name(song_name)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    return jsonify({'songs': results})

# API endpoint to fetch 20 random songs with details
@app.route('/get_random_songs', methods=['GET'])
def get_random_songs():
    if 'user_id' not in session:
        return jsonify({'error': 'User not logged in'}), 401
    try:
        results = fetch_random_songs()
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    return jsonify({'songs': results})

# API endpoint to update points for genre, mood, and artist of a song
@app.route('/update_song_points', methods=['POST'])
def update_song_points():
    # Get JSON payload from the request
    swipe_data = request.json
    # Extract song ID and swipe direction from the payload
    song_id = swipe_data.get('song_id')
    swipe_direction = swipe_data.get('swipe_direction')  # 'left' for decrease, 'right' for increase
    # Validate if 'song_id' and 'swipe_direction' are present in the payload
    if song_id is None or swipe_direction not in ['left', 'right']:
        return jsonify({'error': 'Invalid request payload.'}), 400
    try:
        res = update_points(song_id, swipe_direction)
        if not res:
            return jsonify({'message': 'Failed to update points.'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    return jsonify({'message': 'Points updated successfully.'}), 200

# Endpoint to get a random image
@app.route('/get_random_image', methods=['GET'])
def get_random_image():
    image_files = [f for f in os.listdir(image_folder) if os.path.isfile(os.path.join(image_folder, f))]
    random_image = random.choice(image_files)
    return send_file(os.path.join(image_folder, random_image), mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(debug=True)
