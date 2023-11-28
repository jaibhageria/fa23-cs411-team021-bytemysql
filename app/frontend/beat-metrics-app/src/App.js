// src/components/App.js
import React, { useState, useEffect } from 'react';

const App = () => {
  const [user, setUser] = useState(null);
  const [loginData, setLoginData] = useState({ user_id: '', password: '' });
  const [registrationData, setRegistrationData] = useState({
    user_id: '',
    password: '',
    email: '',
    first_name: '',
    last_name: '',
    phone_number: '',
  });

  useEffect(() => {
    // Check if the user is already logged in on mount
    fetchUserInfo();
  }, []);

  const handleLogin = async () => {
    try {
      const response = await fetch('https://backend-dot-cs411-bytemysql.uc.r.appspot.com/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(loginData),
        credentials: 'include', // Include credentials for cross-origin requests
      });

      if (response.ok) {
        // Login successful
        fetchUserInfo();
      } else {
        // Handle login failure
        console.error('Login failed');
      }
    } catch (error) {
      console.error('Error during login:', error);
    }
  };

  const handleRegistration = async () => {
    try {
      const response = await fetch('https://backend-dot-cs411-bytemysql.uc.r.appspot.com/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(registrationData),
        credentials: 'include', // Include credentials for cross-origin requests
      });

      if (response.ok) {
        // Registration successful, you can optionally handle it here
        console.log('Registration successful');
        // Automatically log in the user after registration
        alert("Registered Successfully, now proceed to login")
      } else {
        // Handle registration failure
        console.error('Registration failed');
      }
    } catch (error) {
      console.error('Error during registration:', error);
    }
  };

  const handleLogout = async () => {
    try {
      const response = await fetch('https://backend-dot-cs411-bytemysql.uc.r.appspot.com/logout', {
        method: 'POST',
        credentials: 'include',
      });

      if (response.ok) {
        // Logout successful
        setUser(null);
      } else {
        // Handle logout failure
        console.error('Logout failed');
      }
    } catch (error) {
      console.error('Error during logout:', error);
    }
  };

  const fetchUserInfo = async () => {
    try {
      const response = await fetch('https://backend-dot-cs411-bytemysql.uc.r.appspot.com/userinfo', {
        method: 'GET',
        credentials: 'include',
      });

      if (response.ok) {
        const user = await response.json();
        setUser(user);
      } else {
        // No user is logged in
        setUser(null);
      }
    } catch (error) {
      console.error('Error fetching user info:', error);
    }
  };

  const displayImage = (base64String) => {
    let input = atob(base64String);
    let binary = new Array();
    for (let i = 0; i < input.length / 2; i++) {
      let h = input.substr(i * 2, 2);
      binary[i] = parseInt(h, 16);
    }
    let byteArray = new Uint8Array(binary);
    return base64String ? <img src={window.URL.createObjectURL(new Blob([byteArray], { type: 'application/octet-stream' }))} alt="User" /> : null;
  };

  return (
    <div>
      {user ? (
        <div>
          <h2>User Info</h2>
          <p>Email: {user.email}</p>
          <p>First Name: {user.first_name}</p>
          <p>Last Name: {user.last_name}</p>
          <p>Phone Number: {user.phone_number}</p>
          <p>User ID: {user.user_id}</p>
          <p>{displayImage(user.picture)}</p>

          <button onClick={handleLogout}>Logout</button>
        </div>
      ) : (
        <div>
          <h2>Login</h2>
          <input
            type="text"
            placeholder="User ID"
            value={loginData.user_id}
            onChange={(e) => setLoginData({ ...loginData, user_id: e.target.value })}
          />
          <input
            type="password"
            placeholder="Password"
            value={loginData.password}
            onChange={(e) => setLoginData({ ...loginData, password: e.target.value })}
          />
          <button onClick={handleLogin}>Login</button>

          <h2>Registration</h2>
          <input
            type="text"
            placeholder="User ID"
            value={registrationData.user_id}
            onChange={(e) => setRegistrationData({ ...registrationData, user_id: e.target.value })}
          />
          <input
            type="password"
            placeholder="Password"
            value={registrationData.password}
            onChange={(e) => setRegistrationData({ ...registrationData, password: e.target.value })}
          />
          <input
            type="text"
            placeholder="Email"
            value={registrationData.email}
            onChange={(e) => setRegistrationData({ ...registrationData, email: e.target.value })}
          />
          <input
            type="text"
            placeholder="First Name"
            value={registrationData.first_name}
            onChange={(e) => setRegistrationData({ ...registrationData, first_name: e.target.value })}
          />
          <input
            type="text"
            placeholder="Last Name"
            value={registrationData.last_name}
            onChange={(e) => setRegistrationData({ ...registrationData, last_name: e.target.value })}
          />
          <input
            type="text"
            placeholder="Phone Number"
            value={registrationData.phone_number}
            onChange={(e) => setRegistrationData({ ...registrationData, phone_number: e.target.value })}
          />
          <button onClick={handleRegistration}>Register</button>
        </div>
      )}
    </div>
  );
};

export default App;
