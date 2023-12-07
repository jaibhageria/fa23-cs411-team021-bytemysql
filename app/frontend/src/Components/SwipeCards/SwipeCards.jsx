import React from "react";
import { useState, useMemo, useRef } from "react";
import TinderCard from "react-tinder-card";
import "./SwipeCard.css";

function SwipeCards() {
  const [song, setSong] = useState([
    {
      name: "Am I Dreaming",
      url: "https://i1.sndcdn.com/artworks-AAyTmvHkLQVl4pxk-HqH3iQ-t500x500.jpg",
    },
    {
      name: "The Batman",
      url: "https://linkstorage.linkfire.com/medialinks/images/edd1f4c6-5f27-4d7d-b79d-56bc519ac60f/artwork-440x440.jpg",
    },
  ]);
  return (
    <>
      <div className="flex flex-col items-center justify-center min-h-screen py-2">
        {song.map((song) => (
          <TinderCard
            className="swipe"
            key={song.name}
            preventSwipe={["up", "down"]}
          >
            <div
              style={{ backgroundImage: `url(${song.url})` }}
              className="card"
            >
              <h3 className="font-display font-semibold text-2xl">
                {song.name}
              </h3>
            </div>
          </TinderCard>
        ))}
      </div>
    </>
  );
}

export default SwipeCards;
