import React, { useState, useEffect } from "react";
import "./ProfilePage.css"; // Make sure to create a ProfilePage.css file for styling
import { useNavigate } from "react-router-dom";

const ProfilePage = () => {
  const [user, setUser] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    // Assume fetchUserInfo is a function that fetches user data from the backend
    fetchUserInfo().then((userInfo) => {
      setUser(userInfo);
    });
  }, []);

  const fetchUserInfo = async () => {
    const response = await fetch(
      "https://backend-dot-cs411-bytemysql.uc.r.appspot.com/user_info",
      {
        method: "GET",
        credentials: "include",
      }
    );
    if (response.ok) {
      const userData = await response.json();
      return userData;
    } else {
      // Handle errors or no user data
      console.error("Failed to fetch user info");
      return null;
    }
  };

  const handleLogout = async () => {
    try {
      // Call the backend API to logout the user
      const response = await fetch(
        "https://backend-dot-cs411-bytemysql.uc.r.appspot.com/logout",
        {
          method: "POST",
          credentials: "include", // Required for cookies to be sent and received
        }
      );

      // Check if the logout was successful
      if (response.ok) {
        // Logout was successful
        console.log("Logout successful");
        navigate("/");
        // Update the state to reflect that the user is no longer logged in
        setUser(null);

        // Optionally, redirect the user to the login page or another appropriate page
        // This depends on your routing setup. For example, using react-router:
        // navigate('/login'); // `navigate` is from useNavigate hook from react-router-dom
      } else {
        // Handle logout failure
        console.error("Logout failed", await response.text());
      }
    } catch (error) {
      // Handle errors in the logout process
      console.error("Error during logout:", error);
    }
  };

  if (!user) return <div>Loading...</div>;

  return (
    <div className="profile-page">
      <div className="username-circle">
        {user.user_id.charAt(0).toUpperCase()}
      </div>
      <div className="user-details">
        <h2>
          {user.first_name} {user.last_name}
        </h2>
        <p>Email: {user.email}</p>
        <p>Phone: {user.phone_number}</p>
        {/* Other user details */}
      </div>
      <button onClick={handleLogout}>Logout</button>
    </div>
  );
};

export default ProfilePage;
