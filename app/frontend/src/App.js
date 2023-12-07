import Explore from "./Components/Explore";
import Header from "./Components/Header";
import Home from "./Components/Home";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { ThemeProvider } from "@material-tailwind/react";
import Login from "./Components/Login";
import Signup from "./Components/SignUp";
import GenreSelection from "./Components/genreselection";
import ArtistSelection from "./Components/artistselection";
import MoodSelection from "./Components/moodselection";
import DashBoard from "./Components/DashBoard";
import ConfirmationPage from "./Components/ConfirmationPage";
import ExplorePage from "./Components/Explore";
import ProfilePage from "./Components/ProfilePage";

function App() {
  return (
    <ThemeProvider>
      <div className="App">
        <Header />
        <Router>
          <Routes>
            <Route path="/" element={<Login />} />
            <Route path="/signup" element={<Signup />} />
            <Route path="/home" element={<Home />} />
            <Route path="/explore" element={<Explore />} />
            <Route path="/dashboard" element={<DashBoard />} />
            <Route path="/genreselection" element={<GenreSelection />} />
            <Route path="/artistselection" element={<ArtistSelection />} />
            <Route path="/moodselection" element={<MoodSelection />} />
            <Route path="/ConfirmationPage" element={<ConfirmationPage />} />
            <Route path="/Explore" element={<ExplorePage />} />
            <Route path="/Profile" element={<ExplorePage />} />
            <Route path="/ProfilePage" element={<ProfilePage />} />
          </Routes>
        </Router>
      </div>
    </ThemeProvider>
  );
}

export default App;
