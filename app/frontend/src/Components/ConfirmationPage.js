import React from "react";
import { useNavigate } from "react-router-dom";

function ConfirmationPage() {
  const navigate = useNavigate();
  return (
    <div>
      <h4>You are all set!</h4>
      <h3>Your preferences have been recorded ! </h3>
      <button onClick={() => navigate("/Explore")}>
        GO BACK TO BROWSE THROUGH MUSIC PERSONALISED FOR YOU!!{" "}
      </button>
    </div>
  );
}

export default ConfirmationPage;
