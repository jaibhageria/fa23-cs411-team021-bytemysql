# Stage 1: Project Proposal: BeatMetrics
> Project Description for Team021 bytemysql

## :memo: Project Title: BeatMetrics

## Project Summary
Our web application redefines the music listening experience with a plethora of features aimed at making it more enjoyable and personalized. Users can easily create and manage playlists, collaborate with others, and explore music tailored to their mood and preferences. We provide insightful statistics, offering a glimpse into their music habits, from favored genres to peak listening hours. As a bonus, premium users can unlock offline listening for an uninterrupted experience.

What sets us apart is our innovative Tinder-like feature for music discovery. Users can swipe right for songs they love, left for those they don't, or simply skip tracks they're undecided about. These swipes shape personalized recommendations based on various song attributes like artist, genre, energy, and more. This engaging feature adds a fun twist to music discovery, setting our platform apart from the rest.

Our application also offers seamless login options, intuitive exploration, and in-depth dashboard insights. Playlist creation is a breeze, with each playlist having its dedicated schema. Users can invite others to join playlists through smart database relationships. Explore top songs, trends, and even filter them by artist popularity or streams per song. Our premium tier, accessible via Stripe, grants exclusive features like offline listening, catering to the diverse needs of music enthusiasts.

## Description
Our application is designed to revolutionize the music listening experience by addressing the common challenges users face in discovering new music and personalizing their playlists. The primary problem we want to solve is the overwhelming abundance of music choices and the lack of tailored recommendations, making it challenging for users to curate their ideal playlists and explore new tracks that resonate with their preferences.

## Features
- **Login/Signup**: Login to the page using email/ id password or google login.
- **Explore**: Explore different songs according to the atmosphere/theme you want or according to the artist. 
- **Personalised recommendations**: Swipe right if you like the song and swipe left if you dislike the song. This information will be used to give recommendations to the user. 
- **User profile/ Dashboard**: Gives information about the user and his/her listening preferences. Information like which genre which the user preferred more or the artists he/she spent more time listening to. It can also give information about total number of hours the user heard music for. 
- **Playlist creation and management**: The user can create a playlist and can also collaborate with other users for creation/management of the playlist. 
- **Music trends and charts**: 	Displaying popular songs and charts.
Top songs by genre or region.Weekly or monthly music trends.
- **Playlist filtering**: The top songs can be filtered on the basis of the number of followers the artist has, or the number of streams per song, etc. 
- **Premium customers**: Can have premium and non-premium customers. Can integrate stripe payment to get subscription, if you have subscribed - special features like offline listening. 

## Usefulness
Our song app offers practicality and convenience by revolutionizing the music listening experience. We aim to provide users with a platform that combines the best features of existing music apps while introducing innovative elements to enhance their overall enjoyment.
Our application goes beyond the standard music streaming platforms. It's designed to simplify music discovery, personalization, and management. Users no longer need to switch between different apps to explore new songs, create playlists, and analyze their listening habits. Our app offers all these functionalities seamlessly integrated into one platform.
Our project addresses the need for a modern and user-centric music streaming service. Existing platforms may have limitations and lack certain features that users desire. We aspire to develop a music app that caters to these needs, offering a more contemporary and user-friendly experience. We hope that our application can set a new standard for music streaming and serve as a proof-of-concept for a system that can be embraced by music enthusiasts worldwide.
Basic key points include: 
1. Playlist Curation: We are able to curate customized playlists for the users who input their preferences into the system. This is a one time process when a user account is created and allows for song recommendations based on the preferences indicated by the user. The user will continue to receive new recommendations based on these preference
2. Enhanced Music Discovery: Users often struggle to discover new music that aligns with their tastes. Our application's Tinder-like feature and advanced recommendation system make it easier for users to find songs they love, ensuring an enriched music discovery experience.
3. User dashboard: The user can see their entire account activity in a glance through the dashboard which will contain information about listening hours, playlists listened to etc.

## Realness
Our database is populated by data from real Spotify users and their listening activity. We will also be adding additional information on user preferences post the account creation which will be randomly generated by us since we cannot get actual user information due to privacy concerns. So the email ids, passwords and song preferences will be randomly generated by the project team for the duration of this project. If deployed, then it will be based on real-time data.

## Basic functions of our web application
The web application provides the users with the basic simple functionalities of creating playlists, collaborating with others, exploring music, viewing the top charts, etc. Along with that, we also show the user statistics that showcase their listening history. It will show them which genres they listened to more, the mood of the songs they played, a comparison of the average number of hours according to the day or the week. We will also have an option where users can pay to have premium features like downloading their songs. In addition to that, the users will also be able to get recommendations on the basis of many features, basic features like genre and advanced features like energy, liveliness, acousticness , etc. The users will have an interface which will help them choose the songs they like and then based on their choices, the users will get the recommendations by the system.

## A good creative component
In recommending songs to the user, we want to give them an experience that will keep them interested in using the application and keep them involved, thereby improving their experience. We want to add a tinder-like functionality where the user can right swipe on the songs that he/she likes and left swipe on the songs that he/she doesn’t like. The user can also skip songs if he/she doesn’t have an opinion on it yet. Our system will use these inputs given by the user and update the database accordingly. Then it will check the features of the songs they liked like artist, genre, and other advanced features like energy, liveliness, speachiness, tempo, loudness, etc and then create an average threshold value of all the songs liked by the user for each attribute. Then it can use these threshold values along with other methods to recommend songs to the user. The Tinder-like functionality adds an element of excitement and novelty to the music discovery process, setting our application apart from traditional music listening platforms.

## Functionality
To further explain the functionality of the entire application, the users will sign in using a login/sign up page. They can sign in using google/Facebook or the traditional way. 
If the user doesn’t exist in the database, a new record will be added to the table with the information of the user when the user signs up. The choices of themes/artists etc that the user made while signing up will also be stored which will be used later. 
For the home/ explore page, the songs will be shown according to moods, top trends, etc. We will get this by applying querying on the database where the songs can be filtered according to themes, moods , artists, etc using selection queries. The users will also be able to filter according to number of streams, country, etc using similar queries. 
Then, the dashboard part of the application will show statistics related to the music listening habits of the user. We will store the songs that the user heard, attributes related to the song etc in another database and then use this to apply aggregation queries, to get details like average hours in a week or most listened to genre, etc. 
In our new functionality of using a tinder-like application, we will create a schema for storing the songs disliked and their attributes, and the song liked and their attributes and a attribute column which shows the choice made by the user. Using these details, we can then show recommendations to the user by performing querying on this. We can also update these values if the user changes his mind later. 
For playlist creation, each playlist will have its own schema and It will be created one the user creates a playlist, the user can add new songs, can delete, update. The user can also add other users and they will be related to the playlist using foreign key and primary key concepts. 
For premium users, there will be an attribute in the user table which will show if the user is premium or not. If the user is premium, only then the option of offline listening will be available to the user.

## Database description
We will store the data in the following tables:
1. User table: all login and song preference information
	```sql
    user_id INT,
	name VARCHAR(255),
    	password VARCHAR(255),
    	email VARCHAR(255),
         activity_id INT,
         Premium BOOLEAN
    ```

2. Song information table: all song information such as title, artist, length, year released, genre tags
      ```sql
        song_id INT,
        song_title VARCHAR(255),
        artist_id INT,
        album_id INT,
        release_date DATE,
        genre VARCHAR(255),
        mood VARCHAR(255),
        number_of_streams INT,
        country VARCHAR(255),
    ```


3. Artists Table: This table stores information about artists. It can include columns like:
```sql
artist_id  INT,
artist_name VARCHAR(255),
song_id INT,
genre VARCHAR(255),
country VARCHAR(255),
Streams  INT
```

4. Listening activity table: user id along with each song the user has listened to and the number of times it was listened to
	```sql
    activity_id INT,
	song_id INT,
    	user_id INT,
    	number_of_times_listened INT
    ```

5. user Preferences Table: This table stores information about users' preferences and filters. It can include columns like:
```sql
user_id  INT, 
preferred_mood VARCHAR(255),
preferred_theme VARCHAR(255),
preferred_artist VARCHAR(255),
preferred_genres VARCHAR(255),
disliked_theme VARCHAR(255),
disliked_artist VARCHAR(255),
disliked_genres VARCHAR(255),
disliked_mood VARCHAR(255),
max_streams INT
```


6. Playlist table: apart from the song ids in the playlist each playlist will be associated with a creator user and collaborator users for convenience in accessing during dashboard display
	```sql
    playlist_id INT,
   	 song_id INT,
         artist_id INT
   	 creator_id INT,
    	collaborator_id INT
    ```


### UI Mockup of BeatMetrics

#### Intro Page
<img width="845" alt="Into Page" src="https://github.com/rahulkumarvh/MDBA-App/assets/66205950/f349a0f6-0a6e-426e-9431-9d426a26d8c3">

#### Sign Up Page
<img width="836" alt="Screenshot 2023-09-13 at 10 55 28 PM" src="https://github.com/rahulkumarvh/MDBA-App/assets/66205950/b51a2d6f-2be2-4079-9dea-e38fa4fd0a48">

#### Login Page
<img width="871" alt="Login" src="https://github.com/rahulkumarvh/MDBA-App/assets/66205950/c0f1a0ee-3f90-485a-a76a-ef2855ae41c2">

#### User Prefrence Prompt (Genre)
<img width="884" alt="Screenshot 2023-09-13 at 10 57 02 PM" src="https://github.com/rahulkumarvh/MDBA-App/assets/66205950/247b7a15-37fe-4ac4-88f0-3b809bd0f050">

#### User Prefrence Prompt (Artist)
<img width="861" alt="Screenshot 2023-09-13 at 10 58 32 PM" src="https://github.com/rahulkumarvh/MDBA-App/assets/66205950/fc7735a1-408b-427b-970c-63c6c8b9f9be">

#### User Prefrence Prompt (Mood)
<img width="867" alt="Screenshot 2023-09-13 at 10 59 08 PM" src="https://github.com/rahulkumarvh/MDBA-App/assets/66205950/114e85f8-069a-437c-a1c3-a4ea2123de70">

#### Home Page
<img width="588" alt="Screenshot 2023-09-13 at 11 00 17 PM" src="https://github.com/rahulkumarvh/MDBA-App/assets/66205950/8f15a80e-59ff-4eff-9172-22fe4b439db3">

#### User Profile
![IMG_0163](https://github.com/rahulkumarvh/MDBA-App/assets/66205950/37bfb2d2-43ed-4f2a-b021-3064d51dfc67)

#### Explore Page
<img width="633" alt="Screenshot 2023-09-13 at 11 08 08 PM" src="https://github.com/rahulkumarvh/MDBA-App/assets/66205950/d8e3d9fa-d3fe-4e13-be79-effcd49b9624">

#### Library Page
<img width="628" alt="Screenshot 2023-09-13 at 11 08 48 PM" src="https://github.com/rahulkumarvh/MDBA-App/assets/66205950/b96874a7-3c86-4d33-b11a-d1cbf60c9cba">

#### Library (Top Songs)
<img width="624" alt="Screenshot 2023-09-13 at 11 09 23 PM" src="https://github.com/rahulkumarvh/MDBA-App/assets/66205950/f7a5eb48-8259-4400-a069-ae83c6d519c3">

#### Library (Top Playlist)
![IMG_0167](https://github.com/rahulkumarvh/MDBA-App/assets/66205950/43ab4589-d67b-4abf-865d-1f7dfbbf5f84)

#### Library (Top Mood)
![IMG_0166](https://github.com/rahulkumarvh/MDBA-App/assets/66205950/4bbb7aae-3aa1-4af9-bebe-66bb7d6afaee)

### Project Distribution

#### Database Management (Backend): 
Implement and manage the database operations based on API requests. This includes handling user preferences, song data, and user interactions like likes and dislikes.
> Responsibility: Rahul (rkv7), Jai (jaia4)
#### Test Data Generation (Backend):
Automatic generate data in the database.
> Responsibility: Mitali (mnm11), Khushi (ksidana2)
#### System Control Flow (Backend):
Implement system-level control flow, including authentication, authorization, and access control. Ensure that user interactions are secure and follow proper access protocols.
> Responsibility: Khushi (ksidana2), Jai (jaia4)
#### Backend API Development:
Create and maintain the backend API. This includes handling requests from the frontend, processing user actions (e.g., likes, dislikes), and generating recommendations based on user preferences.
> Responsibility: Rahul (rkv7), Mitali (mnm11)
#### Frontend UI Design:
Design the user interface (UI) for the web app. Create visually appealing and user-friendly screens for song selection, swiping, and interacting with the recommender system.
> Responsibility: Rahul (rkv7), Khushi (ksidana2)
#### Frontend-Backend Integration:
Design the user interface (UI) for the web app. Create visually appealing and user-friendly screens for song selection, swiping, and interacting with the recommender system.
> Responsibility: Jai (jaia4), Mitali (mnm11)
#### Recommender System Development (Backend):
Build the recommender system that analyzes user likes and dislikes to suggest songs and artists. This involves data analysis and machine learning components.
> Responsibility: Jai (jaia4), Rahul (rkv7), Mitali (mnm11), Khushi (ksidana2)
#### Dashboard Development (Frontend):
Design the user interface (UI) for the web app. Create visually appealing and user-friendly screens for song selection, swiping, and interacting with the recommender system.
> Responsibility: Rahul (rkv7), Khushi (ksidana2), Mitali (mnm11)



