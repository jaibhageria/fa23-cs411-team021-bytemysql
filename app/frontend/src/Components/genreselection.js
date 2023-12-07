import React, { useState, useEffect } from "react";
import "./genreselection.css";
import { useNavigate } from "react-router-dom";

function getRandomColor() {
  const r = Math.floor(Math.random() * 206 + 50);
  const g = Math.floor(Math.random() * 206 + 50);
  const b = Math.floor(Math.random() * 206 + 50);
  return `rgb(${r},${g},${b})`;
}

function GenreSelection() {
  const [genres, setGenres] = useState([]);
  const [user, setUser] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    // If not using context
    fetchUserInfo();
  }, []);

  const [selectedGenres, setSelectedGenres] = useState([]);

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

  useEffect(() => {
    fetch(
      "https://backend-dot-cs411-bytemysql.uc.r.appspot.com/fetch_options",
      {
        method: "GET", // or 'POST' if needed
        credentials: "include", // This sends cookies with the request.
      }
    )
      .then((response) => {
        // Check if the response is ok (status code 200-299)
        if (!response.ok) {
          throw new Error("Network response was not ok " + response.statusText);
        }
        return response.json();
      })
      .then((data) => {
        setGenres(data.genre || []); // Update state with genres data
      })
      .catch((error) => {
        console.error("Error fetching genres:", error);
      });
  }, []);
  // The updated rows array to match the desired number of circles per row
  const rows = [
    [0, 1], // 2 circles in the first row
    [2, 3, 4], // 3 circles in the second row
    [5, 6, 7], // 3 circles in the third row
    [8, 9], // 2 circles in the fourth row
  ];

  const toggleGenreSelection = (genreId) => {
    if (selectedGenres.includes(genreId)) {
      setSelectedGenres(selectedGenres.filter((id) => id !== genreId));
    } else if (selectedGenres.length < 3) {
      setSelectedGenres([...selectedGenres, genreId]);
    }
  };

  const submitGenres = async () => {
    try {
      const response = await fetch(
        "https://backend-dot-cs411-bytemysql.uc.r.appspot.com//set_preference",
        {
          method: "POST",
          credentials: "include",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ genre: selectedGenres }),
        }
      );

      if (response.ok) {
        // Handle successful submission
        navigate("/artistselection");
      } else {
        // Handle error
        console.error("Error submitting genres");
      }
    } catch (error) {
      console.error("Error:", error);
    }
  };

  // Fu
  // The rest of your component remains the same

  return (
    <div className="genres">
      <div className="choose">
        <h4>
          Lets get you started! Let us know your choices so we can recommend
          songs you like
        </h4>
        <h3>Pick 3 of your favourite genres !!</h3>
        <div className="buttons">
          <button onClick={() => navigate("/home")}>PREVIOUS </button>
          <button onClick={submitGenres}>NEXT</button>
        </div>
      </div>
      <div className="genre-container">
        {rows.map((row, rowIndex) => (
          <div key={rowIndex} className="genre-row">
            {row.map((index) => {
              const genreObject = genres[index];
              const isSelected = selectedGenres.includes(genreObject?.genre_id);
              return (
                <div
                  key={index}
                  className={`genre-circle ${isSelected ? "selected" : ""}`}
                  style={{ backgroundColor: getRandomColor() }}
                  onClick={() => toggleGenreSelection(genreObject?.genre_id)}
                >
                  {genreObject ? genreObject.genre_name : "error"}
                </div>
              );
            })}
          </div>
        ))}
      </div>
    </div>
  );
}

export default GenreSelection;
