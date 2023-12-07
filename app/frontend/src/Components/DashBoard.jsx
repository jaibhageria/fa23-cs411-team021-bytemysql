import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

function DashBoard() {
  const [search, setSearch] = useState("");
  const [filterType, setFilterType] = useState("artist");
  const [number, setNumber] = useState("");
  const [searchResults, setSearchResults] = useState([]);
  const [error, setError] = useState("");
  const [user, setUser] = useState(null);
  const [topSongs, setTopSongs] = useState([]);
  const navigate = useNavigate();

  // If using context
  // const { user } = useContext(UserContext);

  useEffect(() => {
    fetchUserInfo();
  }, []);

  const fetchUserInfo = async () => {
    try {
      const response = await fetch(
        "https://backend-dot-cs411-bytemysql.uc.r.appspot.com/user_info",
        {
          method: "GET",
          credentials: "include",
        }
      );

      if (response.ok) {
        const userData = await response.json();
        setUser(userData);
      } else {
        console.error("Error fetching user info");
      }
    } catch (error) {
      console.error("Error:", error);
    }
  };

  const handleSearch = async () => {
    try {
      // Check if the user is logged in
      if (!user) {
        setError("User not logged in");
        return;
      }

      // Fetch songs using your API endpoint
      const response = await fetch(
        "https://backend-dot-cs411-bytemysql.uc.r.appspot.com/search_song?filter=${filterType}&search=${search}&number=${number}",
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
          credentials: "include",
        }
      );

      if (!response.ok) {
        throw new Error(Error);
      }

      const data = await response.json();
      setSearchResults(data.songs);
      setError("");
    } catch (error) {
      setSearchResults([]);
      setError(error.message || "An error occurred while fetching songs.");
    }
  };
  useEffect(() => {
    fetchTopSongs();
    fetchUserInfo();
  }, []);

  const fetchTopSongs = async () => {
    try {
      const response = await fetch(
        "https://backend-dot-cs411-bytemysql.uc.r.appspot.com/top_songs",
        {
          method: "GET",
        }
      );

      if (response.ok) {
        const data = await response.json();
        setTopSongs(data.songs);
      } else {
        console.error("Error fetching top songs");
      }
    } catch (error) {
      console.error("Error:", error);
    }
  };

  const [playlistName, setPlaylistName] = useState("");
  const [selectedSong, setSelectedSong] = useState("");
  const [playlists, setPlaylists] = useState(() => {
    const storedPlaylists = localStorage.getItem("playlists");
    return storedPlaylists ? JSON.parse(storedPlaylists) : [];
  });

  useEffect(() => {
    localStorage.setItem("playlists", JSON.stringify(playlists));
  }, [playlists]);

  const createPlaylist = () => {
    if (playlistName.trim() === "") return;

    setPlaylists([...playlists, { name: playlistName, songs: [] }]);
    setPlaylistName("");
  };

  const addSongToPlaylist = (playlistIndex) => {
    if (selectedSong.trim() === "") return;

    const updatedPlaylists = [...playlists];
    updatedPlaylists[playlistIndex].songs.push(selectedSong);
    setPlaylists(updatedPlaylists);
    setSelectedSong("");
  };

  const removePlaylist = (playlistIndex) => {
    const updatedPlaylists = playlists.filter(
      (_, index) => index !== playlistIndex
    );
    setPlaylists(updatedPlaylists);
  };

  return (
    <div className="flex flex-col items-center justify-center h-screen bg-gray-100">
      <div className="text-4xl pt-8 font-display font-bold text-gray-900">
        {user && (
          <div className="text-4xl pb-2 font-display font-bold text-gray-900">
            {user.first_name}'s Playlist'
          </div>
        )}
      </div>
      <div className="bg-white p-8 rounded shadow-lg">
        <div className="font-bold text-2xl mb-4">Create Playlist</div>
        <div className="flex items-center mb-4">
          <input
            type="text"
            placeholder="Playlist Name"
            value={playlistName}
            onChange={(e) => setPlaylistName(e.target.value)}
            className="mr-2 p-2 border border-gray-300 rounded"
          />
          <button
            onClick={createPlaylist}
            className="bg-blue-500 text-white p-2 rounded"
          >
            Create Playlist
          </button>
        </div>
      </div>

      <div className="bg-white p-8 mt-8 rounded shadow-lg">
        <h2 className="font-bold text-2xl mb-4">Add Song to Playlist</h2>
        <div className="flex items-center mb-4">
          <select
            value={selectedSong}
            onChange={(e) => setSelectedSong(e.target.value)}
            className="mr-2 p-2 border border-gray-300 rounded"
          >
            <option value="">Select a Song</option>
            {songs.map((song, index) => (
              <option key={index} value={song}>
                {song}
              </option>
            ))}
          </select>
          <h3 className="mr-2">Select Playlist:</h3>
          <ul>
            {playlists.map((playlist, index) => (
              <li key={index} className="mb-2">
                {playlist.name}
                <button
                  onClick={() => addSongToPlaylist(index)}
                  className="bg-green-500 text-white p-2 rounded mx-2"
                >
                  Add Song
                </button>
                <button
                  onClick={() => removePlaylist(index)}
                  className="bg-red-500 text-white p-2 rounded"
                >
                  Remove Playlist
                </button>
              </li>
            ))}
          </ul>
        </div>
      </div>

      <div className="bg-white p-8 mt-8 rounded shadow-lg">
        <h2 className="font-bold text-2xl mb-4">Playlists</h2>
        {playlists.map((playlist, index) => (
          <div key={index} className="mb-4">
            <h3 className="font-bold text-xl">{playlist.name}</h3>
            <ul>
              {playlist.songs.map((song, songIndex) => (
                <li key={songIndex} className="ml-4">
                  {song}
                </li>
              ))}
            </ul>
          </div>
        ))}
      </div>
    </div>
  );
}

export default DashBoard;
