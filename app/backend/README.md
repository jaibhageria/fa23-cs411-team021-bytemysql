# Backend setup steps

## Dependencies setup
Run the following commands in order in app/backend:
```python
python3 -m venv env
source env/bin/activate
cd code
pip install -r requirements.txt
```

## Run locally
- For running the app on local system, make sure your IP is whitelisted on the SQL instance with IP `35.225.155.122`
- You can achieve that by navigating to the SQL instance on the GCP project `cs411-bytemysql` with SQL instance name `spotifydata`
- Now just run the below command in app/backend/code:
  ```python
  python3 main.py
  ```

## Run app on Google App Engine (GAE)
- Install the `gcloud` CLI tool compatible for your system
- Run the below command to set the project ID:
  ```bash
  gcloud config set project cs411-bytemysql
  ```
  You may be prompted to sign-in before the above command can run
- To deploy:
  ```bash
  cd app/backend/code
  gcloud app deploy
  ```

That's it!
You can use `gcloud app browse` to hit the URL of the service deployed. This will re-direct to your default browser.
Further, you may find the following list of commands useful:
```bash
# List the services deployed on GAE
gcloud app services list
# List the versions of the services deployed on GAE and their current status
gcloud app versions list
# Stop all services
gcloud app services stop
# Stop a particular service version
gcloud app versions stop <version id from versions list> # example: gcloud app versions stop 20231127t033136
```
For more operations navigate to the app engine dashboard on your GCP project

## Useful SQL commands:

```sql
-- Show stored procedure status
SHOW PROCEDURE STATUS LIKE 'GetSongRecommendations'\G
-- Show the stored procedure code
SHOW CREATE PROCEDURE GetSongRecommendations\G
-- Remove a stored procedure
DROP PROCEDURE IF EXISTS GetSongRecommendations;
-- List all triggers
SHOW TRIGGERS;
-- Remove a particular trigger
DROP TRIGGER playlistMax;
```

## API Documentation:

Login, register, logout APIs:
```bash
# Login
POST /login {"user_id": "foo", "password": "bar"}
# Register
POST /register {"user_id": "foo", "password": "bar", "email": "foo@bar.com", "first_name": "foo", "last_name": "bar", "phone_number": "1234567890"}
# Logout
POST /logout
```

APIs that don't require login:
```bash
# Just display welcome message
GET /
# Just fetches 15 songs from the database based on nothing, topsongs is a misnomer
GET /top_songs
# Fetch the top 15 artists overall based on number of listeners
GET /top_artists
```

APIs tha require login:
```bash
# Get user information, this has an image as well which can be displayed on frontend
GET /userinfo
# Get song recommendations for a user
GET /recommendations
# Get list of all the songs and their details from the backend
GET /songs
# Get details of all genres, all moods, and all artists
GET /fetch_options
# Get 20 random songs; will be used in swipe interface
GET /get_random_songs
# Update points for genre, mood and artist for a song
POST /update_song_points {"song_id": 1, "swipe_direction": "left"}
# Search songs based on filters and song names. Filters are artist, genre, mood
GET /search_song?filter=artist&song_name=abc
# Endpoint to get a random image
GET /get_random_image
# Create a new playlist
POST /create_playlist {"playlist_name": "name"}
# Delete a song from a playlist
POST /delete_song {"playlist_id": id, "song_id": id}
# Add a song to a playlist
POST /add_song {"playlist_id": id, "song_id": id}
# Display playlists belonging to a user
GET /playlist
# Set the preferences. All the fields below are optional
POST /set_preference {"genre": [1,2,3], "artist": [1,2,3], "mood": [1,2,3]}
# Get all the songs inside a playlist
GET /playlist_songs?playlist_id=1
# Set user premium or non-premium; 1 for premium, 0 for non-premium
POST /premium {"premium": 1}
```
