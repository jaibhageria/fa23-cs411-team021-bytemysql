import "./Login.css";
import myImage from "./images/landing-page.jpg";
import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

function Login() {
  const [user, setUser] = useState(null);
  const navigate = useNavigate();
  const [loginData, setLoginData] = useState({ user_id: "", password: "" });

  useEffect(() => {
    // Check if the user is already logged in on mount
    fetchUserInfo();
  }, []);

  const handleLogin = async () => {
    try {
      const response = await fetch(
        "https://backend-dot-cs411-bytemysql.uc.r.appspot.com/login",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(loginData),
          credentials: "include",
        }
      );

      if (response.ok) {
        // Login successful
        fetchUserInfo();
        navigate("/home");
      } else {
        // Handle login failure
        console.error("Login failed");
      }
    } catch (error) {
      console.error("Error during login:", error);
    }
  };

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
        const user = await response.json();
        setUser(user);
      } else {
        // No user is logged in
        setUser(null);
      }
    } catch (error) {
      console.error("Error fetching user info:", error);
    }
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    handleLogin();
  };

  const handleChange = (e) => {
    setLoginData({ ...loginData, [e.target.name]: e.target.value });
  };

  return (
    <div className="main-page">
      <div className="login-details">
        <h1>Welcome back to Beat Metrics !</h1>
        <h3> Start your music journey with us !</h3>
        <div className="login-container">
          <h1>Login </h1>
          <form onSubmit={handleSubmit}>
            <input
              type="text"
              placeholder="User ID"
              value={loginData.user_id}
              onChange={(e) =>
                setLoginData({ ...loginData, user_id: e.target.value })
              }
            />
            <input
              type="password"
              placeholder="Password"
              value={loginData.password}
              onChange={(e) =>
                setLoginData({ ...loginData, password: e.target.value })
              }
            />
            <button onClick={handleLogin}>Login</button>

            <h4>
              Do Not Have an Account?{" "}
              <a href="#" onClick={() => navigate("/signup")}>
                Sign up
              </a>
            </h4>
          </form>
        </div>
      </div>
      <div className="landing-image">
        <img src={myImage} />
      </div>
    </div>
  );
}

export default Login;
