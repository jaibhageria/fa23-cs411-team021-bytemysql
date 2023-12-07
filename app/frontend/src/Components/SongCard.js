import React, { useState, useEffect } from "react";
import axios from "axios";
import "./SongCard.css"; // Import the CSS file for styling

const SongCard = ({ song }) => {
  const [imageUrl, setImageUrl] = useState("");

  useEffect(() => {
    const fetchImage = async () => {
      try {
        const response = await axios.get(
          "https://backend-dot-cs411-bytemysql.uc.r.appspot.com/get_random_image",
          { responseType: "blob" }
        );
        setImageUrl(URL.createObjectURL(response.data));
      } catch (error) {
        console.error("Error fetching image: ", error);
      }
    };

    fetchImage();
  }, [song]); // Fetch a new image whenever the song changes

  return (
    <div className="song-card">
      {imageUrl && <img src={imageUrl} alt="Song" />}
      <h2>
        {song.title} by {song.artist_name}
      </h2>

      <div className="song-details">
        <div className="genre">{song.genre_name}</div>
        <div className="mood">{song.mood_name}</div>
      </div>
    </div>
  );
};

export default SongCard;
