import React from "react";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { testdata } from "./testdata";
import {
  Card,
  CardHeader,
  CardBody,
  CardFooter,
  Typography,
  Avatar,
  Tooltip,
} from "@material-tailwind/react";

import { MagnifyingGlassIcon } from "@heroicons/react/24/outline";

import {
  Input,
  Button,
  Chip,
  Tabs,
  TabsHeader,
  Tab,
  IconButton,
} from "@material-tailwind/react";

import {
  Accordion,
  AccordionHeader,
  AccordionBody,
} from "@material-tailwind/react";

import { List, ListItem } from "@material-tailwind/react";

function Icon({ id, open }) {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      strokeWidth={2}
      stroke="currentColor"
      className={`${
        id === open ? "rotate-180" : ""
      } h-5 w-5 transition-transform`}
    >
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        d="M19.5 8.25l-7.5 7.5-7.5-7.5"
      />
    </svg>
  );
}

function Home() {
  const [search, setSearch] = useState("");
  const [filterType, setFilterType] = useState("artist");
  const [number, setNumber] = useState("");
  const [searchResults, setSearchResults] = useState([]);
  const [error, setError] = useState("");
  const [user, setUser] = useState(null);
  const navigate = useNavigate();

  // If using context
  // const { user } = useContext(UserContext);

  useEffect(() => {
    fetchUserInfo();
  }, []);

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

  const handleSearch = async () => {
    try {
      // Check if the user is logged in
      if (!user) {
        setError("User not logged in");
        return;
      }

      // Fetch songs using your API endpoint
      const response = await fetch(
        `https://backend-dot-cs411-bytemysql.uc.r.appspot.com/search_song?filter=${filterType}&search=${search}&number=${number}`,
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
          credentials: "include",
        }
      );

      if (!response.ok) {
        throw new Error(`Error: ${response.status} - ${response.statusText}`);
      }

      const data = await response.json();
      setSearchResults(data.songs);
      setError("");
    } catch (error) {
      setSearchResults([]);
      setError(error.message || "An error occurred while fetching songs.");
    }
  };

  const [recdata, setRecData] = useState([]);
  useEffect(() => {
    fetch("https://backend-dot-cs411-bytemysql.uc.r.appspot.com/top_artists")
      .then((res) => res.json())
      .then((data) => setRecData(data))
      .catch((err) => console.log(err));
  }, []);

  const [recsdata, setSRecData] = useState([]);
  useEffect(() => {
    fetch("https://backend-dot-cs411-bytemysql.uc.r.appspot.com/top_songs")
      .then((res) => res.json())
      .then((data) => setSRecData(data))
      .catch((err) => console.log(err));
  }, []);

  const [songdata, setSongData] = useState([]);
  useEffect(() => {
    fetch("http://127.0.0.1:5000/songtest")
      .then((res) => res.json())
      .then((songdata) => setSongData(songdata))
      .catch((err) => console.log(err));
  }, []);

  const [prefdata, setPrefData] = useState([]);
  useEffect(() => {
    fetch("http://127.0.0.1:5000/preference")
      .then((res) => res.json())
      .then((prefdata) => setPrefData(prefdata))
      .catch((err) => console.log(err));
  }, []);

  const [open, setOpen] = React.useState(null);
  const handleOpen = (value) => setOpen(open === value ? 0 : value);

  const TABS = [
    {
      label: "All",
      value: "all",
      endpoint:
        "https://backend-dot-cs411-bytemysql.uc.r.appspot.com/get_random_songs",
      key: "all",
      field: "title",
    },
    {
      label: "Artist",
      value: "artist",
      endpoint: "http://127.0.0.1:5000/preference",
      key: "artists",
      field: "artist_name",
    },
    {
      label: "Genre",
      value: "genre",
      endpoint: "http://127.0.0.1:5000/preference",
      key: "genre",
      field: "genre_name",
    },
    {
      label: "Mood",
      value: "mood",
      endpoint: "http://127.0.0.1:5000/preference",
      key: "mood",
      field: "mood_name",
    },
  ];

  const [selectedTab, setSelectedTab] = useState(TABS[0].value);
  const [loading, setLoading] = useState(false);

  const handleTabChange = (value) => {
    setSelectedTab(value);
    setLoading(true);
    setOpen(null);

    const endpoint =
      value === "all"
        ? "http://127.0.0.1:5000/songtest"
        : TABS.find((tab) => tab.value === value).endpoint;

    fetch(endpoint)
      .then((res) => res.json())
      .then((data) => {
        if (value === "all") {
          setSongData(data);
        } else {
          setPrefData(data);
        }
      })
      .catch((err) => console.log(err))
      .finally(() => {
        setLoading(false);
      });
  };

  const TABLE_HEADERS = {
    all: [" ", "Song Title", "Artist", "Genre", "Mood"],
    artist: ["ID", "Artist Name"],
    genre: ["ID", "Genre Name"],
    mood: ["ID", "Mood Name"],
  };

  const filteredData =
    selectedTab === "all"
      ? songdata
      : Array.isArray(
          prefdata[TABS.find((tab) => tab.value === selectedTab)?.key]
        )
      ? prefdata[TABS.find((tab) => tab.value === selectedTab)?.key]
      : [];

  const selectPreference = () => {
    navigate("/genreselection");
  };

  return (
    <div>
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="text-4xl pt-8 font-display font-bold text-gray-900">
          {user && (
            <div className="text-4xl pb-2 font-display font-bold text-gray-900">
              Welcome, {user.first_name}!
            </div>
          )}
          <button
          className=" text-sm text-black bg-gray-300 hover:bg-white"
          type="submit" onClick={selectPreference}>
            Select your preference
          </button>
        </div>
        <div className="mx-auto max-w-2xl py-16 sm:py-24 lg:max-w-none lg:pb-28 divide-y-2 divide-black">
          <div className="text-4xl pb-2 font-display font-bold text-gray-900">
            Search
          </div>
          <div className="pt-6">
            <div className="flex flex-col items-center justify-between gap-4 md:flex-row">
              <div className="p-10">
                <div className="pb-6 flex-center">
                  <label htmlFor="search">Search Term:</label>
                  <input
                    type="text"
                    id="search"
                    value={search}
                    onChange={(e) => setSearch(e.target.value)}
                    className="ml-20"
                  />
                </div>
                <div>
                  <label htmlFor="filterType">Filter Type:</label>
                  <select
                    id="filterType"
                    value={filterType}
                    onChange={(e) => setFilterType(e.target.value)}
                    className="ml-24 p-5"
                  >
                    <option value="artist">Artist</option>
                    <option value="genre">Genre</option>
                    <option value="mood">Mood</option>
                    {/* Add other filter types if needed */}
                  </select>
                </div>
                <div className="pt-8">
                  <label htmlFor="number">Number of Songs:</label>
                  <input
                    type="text"
                    id="number"
                    value={number}
                    onChange={(e) => setNumber(e.target.value)}
                    className="ml-10"
                  />
                </div>
                <div className="mt-8">
                  <button onClick={handleSearch}>Search</button>
                </div>
                {error && <p style={{ color: "red" }}>{error}</p>}
                <div>
                  <tbody>
                    <List className="font-display text-black">
                      {searchResults.map((song) => (
                        <ListItem key={song.song_id}>{song.title}</ListItem>
                      ))}
                    </List>
                  </tbody>
                </div>
              </div>
            </div>
          </div>

          {/* <div className="pt-6">
            <div className="flex flex-col items-center justify-between gap-4 md:flex-row">
              <Tabs value={selectedTab} className="w-full md:w-max">
                <TabsHeader className="font-display">
                  {TABS.map(({ label, value }) => (
                    <Tab
                      className="font-display text-black text-md"
                      key={value}
                      value={value}
                      onClick={() => handleTabChange(value)}
                    >
                      &nbsp;&nbsp;{label}&nbsp;&nbsp;
                    </Tab>
                  ))}
                </TabsHeader>
              </Tabs>
              <div className="w-full font-display md:w-3/5 outline-black outline-2">
                <Input
                  label="Search"
                  icon={
                    <MagnifyingGlassIcon className="h-5 w-5 font-display outline-black" />
                  }
                  onChange={(e) => setSearch(e.target.value)}
                  className="font-display text-md outline-black outline-1"
                />
                <Button
                  onClick={() => handleTabChange(selectedTab)} // Add search logic here
                  color="indigo"
                  buttonType="filled"
                  size="regular"
                  rounded={false}
                  block={false}
                  iconOnly={false}
                  ripple="light"
                >
                  Search
                </Button>
              </div>
            </div>

            <table className="mt-8 w-full min-w-max table-auto text-left">
              <thead>
                <tr>
                  {TABLE_HEADERS[selectedTab].map((head, index) => (
                    <th
                      key={index}
                      className="font-display font-bold border-b-2 border-black bg-black-0/50 p-4"
                    >
                      {head}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {(Array.isArray(filteredData) ? filteredData : [])
                  .filter((item) => {
                    if (search === "") {
                      return true; // Include all items when there's no search query
                    } else {
                      const field = TABS.find(
                        (tab) => tab.value === selectedTab
                      )?.field;
                      const fieldValue = item[field]?.toLowerCase();
                      return (
                        fieldValue && fieldValue.includes(search.toLowerCase())
                      );
                    }
                  })
                  .slice(0, 20)
                  .map((item, i) => (
                    <tr
                      className="font-display border-b-2 border-dashed border-black-0/50"
                      key={i}
                    >
                      {selectedTab === "artist" ? (
                        <>
                          <td className="pt-5">{i + 1}</td>
                          <td>{item.artist_name}</td>
                        </>
                      ) : selectedTab === "genre" ? (
                        <>
                          <td className="pt-5">{i + 1}</td>
                          <td>{item.genre_name}</td>
                        </>
                      ) : selectedTab === "mood" ? (
                        <>
                          <td className="pt-5">{i + 1}</td>
                          <td>{item.mood_name}</td>
                        </>
                      ) : (
                        <>
                          <td className={i}>
                            <div className="flex mt-4 items-center gap-3">
                              <div className="flex flex-col">
                                <Typography className="font-display font-medium">
                                  {i + 1}
                                </Typography>
                              </div>
                            </div>
                          </td>
                          <td className={item.title}>
                            <div className="flex mt-4 items-center gap-3">
                              <div className="flex flex-col">
                                <Typography className="font-display font-medium">
                                  {item.title}
                                </Typography>
                              </div>
                            </div>
                          </td>
                          <td className={item.artist.artist_name}>
                            <div className="flex mt-4 items-center gap-3">
                              <div className="flex flex-col">
                                <Typography className="font-display font-medium">
                                  {item.artist.artist_name}
                                </Typography>
                              </div>
                            </div>
                          </td>
                          <td className={item.genre.genre_name}>
                            <div className="flex mt-4 items-center gap-3">
                              <div className="flex flex-col">
                                <Typography className="font-display font-medium">
                                  {item.genre.genre_name}
                                </Typography>
                              </div>
                            </div>
                          </td>
                          <td className={item.mood.mood_name}>
                            <div className="flex mt-4 items-center gap-3">
                              <div className="flex flex-col">
                                <Typography className="font-display font-medium">
                                  {item.mood.mood_name}
                                </Typography>
                              </div>
                            </div>
                          </td>
                        </>
                      )}
                    </tr>
                  ))}
              </tbody>
            </table>
          </div>*/}
        </div>
      </div>

      {/* Top Recommended Artist Section */}
      <div className="bg-gray-100">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="mx-auto max-w-2xl py-16 sm:py-24 lg:max-w-none lg:py-32">
            <div className="text-4xl font-display font-bold text-gray-900">
              Recommended Artists
            </div>
            <div className="p-12 grid grid-cols-7 grid-rows-7 gap-4">
              <div className="col-span-5 row-span-4">
                <Card className="w-full h-96 overflow-hidden">
                  <CardHeader
                    floated={false}
                    shadow={false}
                    color="transparent"
                    className="m-0 rounded-none"
                  >
                    <img
                      src="https://cdn.dribbble.com/userupload/8471416/file/original-dbc1be68394f26034b5892ce7039203a.jpg?resize=2142x300"
                      alt="ui/ux review check"
                      className="object-cover w-full h-72"
                    />
                  </CardHeader>
                  <CardBody>
                    <Typography
                      className="font-display font-bold"
                      variant="h3"
                      color="blue-gray"
                    >
                      Top Artist:
                      {Array.isArray(recdata.artists) &&
                        recdata.artists.length > 0 && (
                          <span> {recdata.artists[0].artist_name}</span>
                        )}
                    </Typography>
                  </CardBody>
                </Card>
              </div>
              <div className="col-span-2 row-span-4 col-start-6">
                <Card className="w-full h-96 overflow-hidden">
                  <CardHeader
                    floated={false}
                    shadow={false}
                    color="transparent"
                    className="m-0 rounded-none"
                  >
                    <img
                      src="https://cdn.dribbble.com/users/938871/screenshots/6666342/loving-dribbble.jpg"
                      alt="ui/ux review check"
                    />
                  </CardHeader>
                  <CardBody>
                    <Typography
                      className="font-display font-bold"
                      variant="h3"
                      color="blue-gray"
                    >
                      {Array.isArray(recdata.artists) &&
                        recdata.artists.length > 0 && (
                          <span>2. {recdata.artists[1].artist_name}</span>
                        )}
                    </Typography>
                  </CardBody>
                </Card>
              </div>
              <div className="col-span-2 row-span-3 row-start-5">
                <Card className="w-full h-96 overflow-hidden">
                  <CardHeader
                    floated={false}
                    shadow={false}
                    color="transparent"
                    className="m-0 rounded-none"
                  >
                    <img
                      src="https://cdn.dribbble.com/users/725870/screenshots/5608414/music_preview.jpg"
                      alt="ui/ux review check"
                    />
                  </CardHeader>
                  <CardBody>
                    <Typography
                      className="font-display font-bold"
                      variant="h3"
                      color="blue-gray"
                    >
                      {Array.isArray(recdata.artists) &&
                        recdata.artists.length > 0 && (
                          <span>3. {recdata.artists[2].artist_name}</span>
                        )}
                    </Typography>
                  </CardBody>
                </Card>
              </div>
              <div className="col-span-2 row-span-3 col-start-3 row-start-5">
                <Card className="w-full h-96 overflow-hidden">
                  <CardHeader
                    floated={false}
                    shadow={false}
                    color="transparent"
                    className="m-0 rounded-none"
                  >
                    <img
                      src="https://cdn.dribbble.com/users/1303513/screenshots/4709378/media/4dc9d7fd004b05a4cbd1dbd5cc69e97c.jpg?resize=800x600&vertical=center"
                      alt="ui/ux review check"
                    />
                  </CardHeader>
                  <CardBody>
                    <Typography
                      className="font-display font-bold"
                      variant="h3"
                      color="blue-gray"
                    >
                      {Array.isArray(recdata.artists) &&
                        recdata.artists.length > 0 && (
                          <span>4. {recdata.artists[3].artist_name}</span>
                        )}
                    </Typography>
                  </CardBody>
                </Card>
              </div>
              <div className="col-span-3 row-span-3 col-start-5 row-start-5">
                <Card className="w-full h-96 overflow-hidden">
                  <CardHeader
                    floated={false}
                    shadow={false}
                    color="transparent"
                    className="m-0 rounded-none"
                  >
                    <img
                      src="https://cdn.dribbble.com/users/31752/screenshots/4032680/media/c66eac28e522faa1b7bffca90bb3816c.jpg"
                      alt="ui/ux review check"
                    />
                  </CardHeader>
                  <CardBody>
                    <Typography
                      className="font-display font-bold"
                      variant="h3"
                      color="blue-gray"
                    >
                      {Array.isArray(recdata.artists) &&
                        recdata.artists.length > 0 && (
                          <span>5. {recdata.artists[4].artist_name}</span>
                        )}
                    </Typography>
                  </CardBody>
                </Card>
              </div>
            </div>
            <Accordion
              className="mt-7 font-display"
              open={open === 1}
              icon={<Icon id={1} open={open} />}
            >
              <AccordionHeader
                className="font-display font-bold text-black text-2xl"
                onClick={() => handleOpen(1)}
              >
                View More
              </AccordionHeader>
              <AccordionBody className="text-black">
                <List className="font-display text-black">
                  {Array.isArray(recdata.artists) &&
                    recdata.artists.slice(5).map((artist, i) => (
                      <tr key={i}>
                        <ListItem>
                          {i + 6}. {artist.artist_name}
                        </ListItem>
                      </tr>
                    ))}
                </List>
              </AccordionBody>
            </Accordion>
          </div>
        </div>
      </div>

      {/* Top Recommended Songs Section */}
      <div className="bg-red-700">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="mx-auto max-w-2xl py-16 sm:py-24 lg:max-w-none lg:py-32">
            <div className="text-4xl font-display font-bold text-white">
              Recommended Songs
            </div>
            <div className="p-12 grid grid-cols-7 grid-rows-7 gap-4">
              <div className="col-span-5 row-span-4">
                <Card className="w-full h-96 overflow-hidden">
                  <CardHeader
                    floated={false}
                    shadow={false}
                    color="transparent"
                    className="m-0 rounded-none"
                  >
                    <img
                      src="https://img.freepik.com/free-vector/colorful-creepy-creatures-illustration-background_516247-10.jpg?w=900&t=st=1701770779~exp=1701771379~hmac=3a9b8a13634ad07460ce2937e9d00c4643f75c1452d1f343c515004a53fdb732"
                      alt="ui/ux review check"
                      className="object-cover w-full h-72"
                    />
                  </CardHeader>
                  <CardBody>
                    <Typography
                      className="font-display font-bold"
                      variant="h3"
                      color="blue-gray"
                    >
                      Top Song:
                      {Array.isArray(recsdata.songs) &&
                        recsdata.songs.length > 0 && (
                          <span> {recsdata.songs[0].title}</span>
                        )}
                    </Typography>
                  </CardBody>
                </Card>
              </div>
              <div className="col-span-2 row-span-4 col-start-6">
                <Card className="w-full h-96 overflow-hidden">
                  <CardHeader
                    floated={false}
                    shadow={false}
                    color="transparent"
                    className="m-0 rounded-none"
                  >
                    <img
                      src="https://cdn.dribbble.com/users/938871/screenshots/9517603/media/3c4c3cfd5773193471f597e3164943e3.jpg"
                      alt="ui/ux review check"
                    />
                  </CardHeader>
                  <CardBody>
                    <Typography
                      className="font-display font-bold"
                      variant="h3"
                      color="blue-gray"
                    >
                      {Array.isArray(recsdata.songs) &&
                        recsdata.songs.length > 0 && (
                          <span>2.{recsdata.songs[1].title}</span>
                        )}
                    </Typography>
                  </CardBody>
                </Card>
              </div>
              <div className="col-span-2 row-span-3 row-start-5">
                <Card className="w-full h-96 overflow-hidden">
                  <CardHeader
                    floated={false}
                    shadow={false}
                    color="transparent"
                    className="m-0 rounded-none"
                  >
                    <img
                      src="https://cdn.dribbble.com/users/123624/screenshots/4680127/mfacrop.jpg"
                      alt="ui/ux review check"
                    />
                  </CardHeader>
                  <CardBody>
                    <Typography
                      className="font-display font-bold"
                      variant="h3"
                      color="blue-gray"
                    >
                      {Array.isArray(recsdata.songs) &&
                        recsdata.songs.length > 0 && (
                          <span>3.{recsdata.songs[2].title}</span>
                        )}
                    </Typography>
                  </CardBody>
                </Card>
              </div>
              <div className="col-span-2 row-span-3 col-start-3 row-start-5">
                <Card className="w-full h-96 overflow-hidden">
                  <CardHeader
                    floated={false}
                    shadow={false}
                    color="transparent"
                    className="m-0 rounded-none"
                  >
                    <img
                      src="https://cdn.dribbble.com/users/26059/screenshots/329896/attachments/14956/dinner_fullcrop.jpg"
                      alt="ui/ux review check"
                    />
                  </CardHeader>
                  <CardBody>
                    <Typography
                      className="font-display font-bold"
                      variant="h3"
                      color="blue-gray"
                    >
                      {Array.isArray(recsdata.songs) &&
                        recsdata.songs.length > 0 && (
                          <span>4.{recsdata.songs[3].title}</span>
                        )}
                    </Typography>
                  </CardBody>
                </Card>
              </div>
              <div className="col-span-3 row-span-3 col-start-5 row-start-5">
                <Card className="w-full h-96 overflow-hidden">
                  <CardHeader
                    floated={false}
                    shadow={false}
                    color="transparent"
                    className="m-0 rounded-none"
                  >
                    <img
                      src="https://cdn.dribbble.com/users/2761/screenshots/12219340/media/8eda375c04c71bbeca14c4c71f0fe876.png"
                      alt="ui/ux review check"
                    />
                  </CardHeader>
                  <CardBody>
                    <Typography
                      className="font-display font-bold"
                      variant="h3"
                      color="blue-gray"
                    >
                      {Array.isArray(recsdata.songs) &&
                        recsdata.songs.length > 0 && (
                          <span>5.{recsdata.songs[4].title}</span>
                        )}
                    </Typography>
                  </CardBody>
                </Card>
              </div>
            </div>
            <Accordion
              className="mt-7 text-white font-display"
              open={open === 1}
              icon={<Icon id={1} open={open} />}
            >
              <AccordionHeader
                className="font-display font-bold text-white text-2xl"
                onClick={() => handleOpen(1)}
              >
                View More
              </AccordionHeader>
              <AccordionBody className="text-white">
                <List className="font-display text-white">
                  {Array.isArray(recsdata.songs) &&
                    recsdata.songs.slice(5).map((songs, i) => (
                      <tr key={i}>
                        <ListItem>
                          {i + 6}. {songs.title}
                        </ListItem>
                      </tr>
                    ))}
                </List>
              </AccordionBody>
            </Accordion>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Home;
