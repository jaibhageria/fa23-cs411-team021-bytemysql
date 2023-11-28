#main.py
from flask import Flask, jsonify, request, session
from db import login_check, check_user_id, add_user_with_pic, fetch_all_songs, get_user_info
from helper import fetch_random_user_image, base64_encode_picture
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Change this to a secure secret key
CORS(app)

@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        if not request.is_json:
            return jsonify({"msg": "Missing JSON in request"}), 400  
    return 'Welcome to BeatMetrics'

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

if __name__ == '__main__':
    app.run(debug=True)

