import { useNavigate } from "react-router-dom";
import myImage from "./images/landing-page.jpg";
import React, { useState } from "react";

function Signup() {
  const navigate = useNavigate();
  const [registrationData, setRegistrationData] = useState({
    user_id: "",
    password: "",
    email: "",
    first_name: "",
    last_name: "",
    phone_number: "",
  });

  const handleInputChange = (e) => {
    setRegistrationData({
      ...registrationData,
      [e.target.name]: e.target.value,
    });
  };

  const handleRegistration = async () => {
    try {
      const response = await fetch(
        "https://backend-dot-cs411-bytemysql.uc.r.appspot.com/register",
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(registrationData),
          credentials: "include",
        }
      );

      if (response.ok) {
        alert("Registered Successfully, now proceed to login");
        navigate("/");
      } else {
        alert("Registration failed");
      }
    } catch (error) {
      console.error("Error during registration:", error);
      alert("An error occurred during registration.");
    }
  };

  const alreadyRegister = () => {
    navigate("/");
  }
  return (
    <div className="main-page">
      <div className="login-details">
        <h1>Welcome to Beat Metrics </h1>
        <h3> Start your music journey with us !</h3>
        <div className="login-container">
          <input
            type="text"
            name="user_id"
            placeholder="Username"
            required
            onChange={handleInputChange}
          />
          <input
            type="email"
            name="email"
            placeholder="Email"
            required
            onChange={handleInputChange}
          />
          <input
            type="password"
            name="password"
            placeholder="Password"
            required
            onChange={handleInputChange}
          />
          <input
            type="text"
            name="first_name"
            placeholder="First Name"
            required
            onChange={handleInputChange}
          />
          <input
            type="text"
            name="last_name"
            placeholder="Last Name"
            required
            onChange={handleInputChange}
          />
          <input
            type="text"
            name="phone_number"
            placeholder="Phone Number"
            required
            onChange={handleInputChange}
          />
          <button type="submit" onClick={alreadyRegister}>Already register? Please login </button>
          <button type="submit" onClick={handleRegistration}>
            Signup
          </button>
        </div>
      </div>
      <div className="landing-image">
        <img src={myImage} />
      </div>
    </div>
  );
}

export default Signup;
