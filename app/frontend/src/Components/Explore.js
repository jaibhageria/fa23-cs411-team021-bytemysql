import React, { useState, useEffect } from "react";
import axios from "axios";
import SongCard from "./SongCard";
import "./Explore.css";
import ProfilePage from "./ProfilePage";
import { useNavigate } from "react-router-dom";

const ExplorePage = () => {
  const [songs, setSongs] = useState([]);
  const [currentSongIndex, setCurrentSongIndex] = useState(0);
  const navigate = useNavigate();

  useEffect(() => {
    fetchRandomSongs();
  }, []);

  const handleSwipe = (direction) => {
    updateSongPoints(direction);
    // Move to next song
    setCurrentSongIndex((prevIndex) => (prevIndex + 1) % songs.length);
  };

  const fetchRandomSongs = async () => {
    try {
      const response = await axios.get(
        "https://backend-dot-cs411-bytemysql.uc.r.appspot.com/get_random_songs",
        { withCredentials: true }
      );
      setSongs(response.data.songs);
      setCurrentSongIndex(0);
    } catch (error) {
      console.error("Error fetching random songs: ", error);
    }
  };

  const updateSongPoints = async (direction) => {
    if (songs.length > 0) {
      try {
        await axios.post(
          "https://backend-dot-cs411-bytemysql.uc.r.appspot.com/update_song_points",
          {
            song_id: songs[currentSongIndex].song_id,
            swipe_direction: direction,
          },
          { withCredentials: true }
        );
        // Move to next song
        setCurrentSongIndex((prevIndex) => (prevIndex + 1) % songs.length);
      } catch (error) {
        console.error("Error updating song points: ", error);
      }
    }
  };

  if (songs.length === 0) return <div>Loading...</div>;

  const currentSong = songs[currentSongIndex];

  return (
    <div className="explore-page ">
      <div className="container">
        <div>
          <SongCard song={currentSong} />
          <div className="buttons">
            <button onClick={() => updateSongPoints("left")}>Dislike</button>
            <button onClick={() => updateSongPoints("right")}>Like</button>
          </div>
        </div>
        <div class="text">
          <h3>Click Like if you like this song and Dislike if you dont</h3>
          <h4>We will save your preferences !</h4>
          <button onClick={() => navigate("/ProfilePage")}>
            Continue browsing music!!
          </button>
        </div>
      </div>
    </div>
  );
};
export default ExplorePage;
