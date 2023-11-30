#main.py
from flask import Flask, jsonify, request, session
from db import *
from helper import fetch_random_user_image, base64_encode_picture
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Change this to a secure secret key
app.config['SESSION_COOKIE_SAMESITE'] = None
CORS(app, supports_credentials=True)

@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        if not request.is_json:
            return jsonify({"msg": "Missing JSON in request"}), 400
    
    # get the recommended songs for this user if logged in else show top 15 songs
    songs = []
    if 'user_id' in session:
        songs = get_recommendations(session['user_id'])
    else:
        songs = get_top15()

    top_artists = get_top_artists()
    return jsonify({'songs': songs, 'artists': top_artists}), 200

    # return 'Welcome to BeatMetrics'

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
@app.route('/userinfo', methods=['GET'])
def userinfo():
    if 'user_id' not in session:
        return jsonify({'message': 'User not logged in'}), 401

    user_id = session['user_id']
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
@app.route("/preference", methods=['GET', 'POST'])
def get_prefs():
    # FOR TESTING --- REMOVE
    session['user_id'] = 'abcd1234'
    if 'user_id' not in session:
        return jsonify({'message': 'User not logged in'}), 401
    
    # backend sends the list of all genres, moods and artists to frontend
    if request.method == 'GET':
        genres = fetch_all_genres()
        moods = fetch_all_moods()
        artists = fetch_all_artists()

        prefs_prompt = {
            "genre": genres,
            "mood": moods,
            "artists": artists
        }

        return jsonify(prefs_prompt), 200

    # recieve the preference selections and update the preference points for that user
    if request.method == 'POST':
        if not request.is_json:
            return jsonify({"msg": "Missing JSON in request"}), 400
        
        data = request.json  #format expected: {"genre": [genre_id1, genre_id2, ...], "artist": [artist_id1, artist_id2, ...], "mood": [mood_id1, mood_id2, ...]}
        ret = update_prefs(data, session["user_id"])

        if ret:
            return jsonify({"message": "preference update successful"}), 200
        else:
            return jsonify({'message': 'there was an error while updating preferences'}), 500

# display the playlists of the current user
@app.route("/playlist", methods=['GET'])
def get_playlists():
    # FOR TESTING --- REMOVE
    session['user_id'] = 'brian95'
    if 'user_id' not in session:
        return jsonify({'message': 'User not logged in'}), 401

    user_id = session['user_id']

    if request.method == 'GET':
        playlists = get_all_playlists(user_id)
        return jsonify(playlists), 200
    

# add a new song to a playlist
@app.route("/addsong", methods=['GET', 'POST'])
def add_song_to_playlist():
    # FOR TESTING --- REMOVE
    session['user_id'] = 'brian95'
    if 'user_id' not in session:
        return jsonify({'message': 'User not logged in'}), 401
    
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    
    data = request.json  #format expected: {"playlist_id": id, "song_id": id}
    if add_to_playlist(data):
        return jsonify({'message': 'succesfully added song to playlist'}), 200
    else:
        return jsonify({'message': 'song could not be added to playlist'}), 500

# delete a song from a playlist
@app.route("/deletesong", methods=['GET', 'POST'])
def delete_song_from_playlist():
    # FOR TESTING --- REMOVE
    session['user_id'] = 'brian95'
    if 'user_id' not in session:
        return jsonify({'message': 'User not logged in'}), 401
    
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    
    data = request.json #format expected: {"playlist_id": id, "song_id": id}
    if delete_from_playlist(data):
        return jsonify({'message': 'succesfully deleted song from playlist'}), 200
    else:
        return jsonify({'message': 'song could not be deleted from playlist'}), 500



if __name__ == '__main__':
    app.run(debug=True)

