#main.py
from flask import Flask, jsonify, request, session, send_file
from db import *
from helper import *
from flask_cors import CORS
import os
import re

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Change this to a secure secret key
app.config['SESSION_COOKIE_SAMESITE'] = None
CORS(app, supports_credentials=True)

# Define the path to the folder containing images
image_folder = os.path.join(os.getcwd(), 'images')

number_pattern = r'^[1-9]\d*$'

@app.route('/', methods=['GET'])
def home():
    return 'Welcome to BeatMetrics'

@app.route('/top_songs', methods=['GET'])
def top_songs():
    try:
        songs = []
        songs = get_top15()
        return jsonify({'songs': songs}), 200
    except Exception as e:
        error(e)
        return jsonify({'error': str(e)}), 500

@app.route('/top_artists', methods=['GET'])
def top_artists():
    try:
        top_artists = []
        top_artists = get_top_artists()
        return jsonify({'artists': top_artists}), 200
    except Exception as e:
        error(e)
        return jsonify({'error': str(e)}), 500

@app.route('/recommendations/<int:num_songs>', methods=['GET'])
def recommendations(num_songs):
    try:
        if 'user_id' not in session:
            return jsonify({'message': 'User not logged in'}), 401
        songs = []
        songs = get_recommendations(session.get('user_id'), num_songs)
        return jsonify({'songs': songs}), 200
    except Exception as e:
        error(e)
        return jsonify({'error': str(e)}), 500

# API endpoint to login
@app.route('/login', methods=['POST'])
def login():
    try:
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
    except Exception as e:
        error(e)
        return jsonify({'error': str(e)}), 500
    
# API endpoint to logout
@app.route('/logout', methods=['POST'])
def logout():
    try:
        if 'user_id' not in session:
            return jsonify({'message': 'User not logged in'}), 401
        session.pop('user_id', None)
        return jsonify({'message': 'Logout successful'}), 200
    except Exception as e:
        error(e)
        return jsonify({'error': str(e)}), 500
    
# API endpoint to register
@app.route('/register', methods=['POST'])
def register():
    try:
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
    except Exception as e:
        error(e)
        return jsonify({'error': str(e)}), 500

# API endpoint to get user information
@app.route('/user_info', methods=['GET'])
def userinfo():
    try:
        if 'user_id' not in session:
            return jsonify({'message': 'User not logged in'}), 401
        user_id = session.get('user_id')
        user = get_user_info(user_id)
        if user:
            user['picture'] = base64_encode_picture(user['picture'])
            return jsonify(user), 200
        else:
            return jsonify({'message': 'User not found'}), 404
    except Exception as e:
        error(e)
        return jsonify({'error': str(e)}), 500

# API endpoint to get all songs
@app.route('/songs', methods=['GET'])
def get_songs():
    try:
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
    except Exception as e:
        error(e)
        return jsonify({'error': str(e)}), 500

# send all genres, moods and artist names and recieve the preferred selections from user
@app.route("/fetch_options", methods=['GET'])
def get_all_options():
    try:
        if 'user_id' not in session:
            return jsonify({'message': 'User not logged in'}), 401
        # backend sends the list of all genres, moods and artists to frontend
        genres = fetch_all_genres()
        moods = fetch_all_moods()
        artists = fetch_all_artists()

        results = {
            "genre": genres,
            "mood": moods,
            "artists": artists
        }
        return jsonify(results), 200
    except Exception as e:
        error(e)
        return jsonify({'error': str(e)}), 500

# send all genres, moods and artist names and recieve the preferred selections from user
@app.route("/set_preference", methods=['POST'])
def set_prefs():
    try:
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
    except Exception as e:
        error(e)
        return jsonify({'error': str(e)}), 500

# display the playlists of the current user
@app.route("/playlist", methods=['GET'])
def get_playlists():
    try:
        if 'user_id' not in session:
            return jsonify({'message': 'User not logged in'}), 401
        user_id = session.get('user_id')
        playlists = get_all_playlists(user_id)
        return jsonify(playlists), 200
    except Exception as e:
        error(e)
        return jsonify({'error': str(e)}), 500

# add a new song to a playlist
@app.route("/add_song", methods=['POST'])
def add_song_to_playlist():
    try:
        if 'user_id' not in session:
            return jsonify({'message': 'User not logged in'}), 401
        user_id = session.get('user_id')
        if request.method == 'POST':
            if not request.is_json:
                return jsonify({"msg": "Missing JSON in request"}), 400
        data = request.json  #format expected: {"playlist_id": id, "song_id": id}
        res = check_user_playlist(data, user_id)[0]
        if res.get('playlist_count') < 1:
            return jsonify({"msg": f"user_id:{user_id} does not own the playlist with playlist_id:{data.get('playlist_id', None)}"}), 400
        status, limit = add_to_playlist(data)
        if status:
            return jsonify({'message': 'succesfully added song to playlist'}), 200
        elif limit:
            return jsonify({'message': 'song could not be added to playlist because max capacity has been reached'}), 200
        else:
            return jsonify({'message': 'song could not be added to playlist'}), 500
    except Exception as e:
        error(e)
        return jsonify({'error': str(e)}), 500

# delete a song from a playlist
@app.route("/delete_song", methods=['POST'])
def delete_song_from_playlist():
    try:
        if 'user_id' not in session:
            return jsonify({'message': 'User not logged in'}), 401
        user_id = session.get('user_id')
        if request.method == 'POST':
            if not request.is_json:
                return jsonify({"msg": "Missing JSON in request"}), 400
        data = request.json #format expected: {"playlist_id": id, "song_id": id}
        res = check_user_playlist(data, user_id)[0]
        if res.get('playlist_count') < 1:
            return jsonify({"msg": f"user_id:{user_id} does not own the playlist with playlist_id:{data.get('playlist_id', None)}"}), 400
        if delete_from_playlist(data):
            return jsonify({'message': 'succesfully deleted song from playlist'}), 200
        else:
            return jsonify({'message': 'song could not be deleted from playlist'}), 500
    except Exception as e:
        error(e)
        return jsonify({'error': str(e)}), 500

# create new empty playlist
@app.route("/create_playlist", methods=['POST'])
def create_playlist():
    try:
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
            return jsonify({'error': 'playlist could not be created'}), 400
    except Exception as e:
        error(e)
        return jsonify({'error': str(e)}), 500
    
# API endpoint to search for a song by name
@app.route('/search_song', methods=['GET'])
def search_songs():
    try:
        if 'user_id' not in session:
            return jsonify({'error': 'User not logged in'}), 401
        search = request.args.get('search', None)
        filter_type = request.args.get('filter', None)
        number = request.args.get('number', None)
        if search is None:
            return jsonify({'error': 'Search string is missing in the request'}), 400
        if filter_type is None or filter_type not in ['song', 'genre', 'artist', 'mood']:
            return jsonify({'error': 'Invalid filter type in payload'}), 400
        if number is None or not re.match(number_pattern, number):
            return jsonify({'error': 'Invalid number type in payload'}), 400
        if filter_type == "song":
            results = find_songs_by_name(search, number)
        elif filter_type == "genre":
            results = find_songs_by_genre(search,number)
        elif filter_type == "artist":
            results = find_songs_by_artist(search, number)
        elif filter_type == "mood":
            results = find_songs_by_mood(search, number)
        return jsonify({'songs': results})
    except Exception as e:
        error(e)
        return jsonify({'error': str(e)}), 500

# API endpoint to fetch 20 random songs with details
@app.route('/get_random_songs', methods=['GET'])
def get_random_songs():
    try:
        if 'user_id' not in session:
            return jsonify({'error': 'User not logged in'}), 401
        results = fetch_random_songs()
        return jsonify({'songs': results})
    except Exception as e:
        error(e)
        return jsonify({'error': str(e)}), 500

# API endpoint to update points for genre, mood, and artist of a song
@app.route('/update_song_points', methods=['POST'])
def update_song_points():
    try:
        if 'user_id' not in session:
            return jsonify({'error': 'User not logged in'}), 401
        if request.method == 'POST':
            if not request.is_json:
                return jsonify({"msg": "Missing JSON in request"}), 400
        user_id = session.get('user_id')
        # Get JSON payload from the request
        swipe_data = request.json
        # Extract song ID and swipe direction from the payload
        song_id = swipe_data.get('song_id')
        swipe_direction = swipe_data.get('swipe_direction')  # 'left' for decrease, 'right' for increase
        # Validate if 'song_id' and 'swipe_direction' are present in the payload
        if song_id is None or swipe_direction not in ['left', 'right']:
            return jsonify({'error': 'Invalid request payload.'}), 400
        res = update_points(song_id, swipe_direction, user_id)
        if not res:
            return jsonify({'message': 'Failed to update points.'}), 200
        return jsonify({'message': 'Points updated successfully.'}), 200
    except Exception as e:
        error(e)
        return jsonify({'error': str(e)}), 500

# Endpoint to get a random image
@app.route('/get_random_image', methods=['GET'])
def get_random_image():
    try:
        image_files = [f for f in os.listdir(image_folder) if os.path.isfile(os.path.join(image_folder, f))]
        random_image = random.choice(image_files)
        return send_file(os.path.join(image_folder, random_image), mimetype='image/jpeg')
    except Exception as e:
        error(e)
        return jsonify({'error': str(e)}), 500

# Endpoint to set user premium/non-premium
@app.route('/premium', methods=['POST'])
def set_premium_status():
    try:
        if 'user_id' not in session:
            return jsonify({'error': 'User not logged in'}), 401
        if request.method == 'POST':
            if not request.is_json:
                return jsonify({"msg": "Missing JSON in request"}), 400
        user_id = session.get('user_id')
        payload = request.json
        is_premium = payload.get('is_premium')
        res = update_premium_status(user_id, is_premium)
        if res:
            return jsonify({'message': 'succesfully updated user premium status'}), 200
        else:
            return jsonify({'message': 'failed to update user premium status'}), 400
    except Exception as e:
        error(e)
        return jsonify({'error': str(e)}), 500
    
# API endpoint to display all songs in a playlist with details
@app.route('/playlist_songs/<int:playlist_id>', methods=['GET'])
def playlist_songs(playlist_id):
    try:
        if 'user_id' not in session:
            return jsonify({'error': 'User not logged in'}), 401
        res = get_playlist_songs(playlist_id)
    except Exception as e:
        error(e)
        return jsonify({'error': str(e)}), 500
    return jsonify({'songs': res}), 200

if __name__ == '__main__':
    app.run(debug=True)
