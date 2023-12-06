
CREATE DATABASE `BeatMetrics`

USE `BeatMetrics`

DROP TABLE IF EXISTS `Artist`;
CREATE TABLE `Artist` (
  `artist_id` int NOT NULL AUTO_INCREMENT,
  `artist_name` varchar(255) NOT NULL,
  `nationality` varchar(255) NOT NULL,
  `genre_id` int NOT NULL,
  PRIMARY KEY (`artist_id`),
  KEY `genre_id` (`genre_id`),
  CONSTRAINT `Artist_ibfk_1` FOREIGN KEY (`genre_id`) REFERENCES `Genre` (`genre_id`)
);

DROP TABLE IF EXISTS `Genre`;
CREATE TABLE `Genre` (
  `genre_id` int NOT NULL AUTO_INCREMENT,
  `genre_name` varchar(255) NOT NULL,
  PRIMARY KEY (`genre_id`)
);

DROP TABLE IF EXISTS `Listens`;
CREATE TABLE `Listens` (
  `listener_id` varchar(255) NOT NULL,
  `song_id` int NOT NULL,
  PRIMARY KEY (`listener_id`,`song_id`),
  KEY `song_id` (`song_id`),
  CONSTRAINT `Listens_ibfk_1` FOREIGN KEY (`listener_id`) REFERENCES `User` (`user_id`) ON DELETE CASCADE,
  CONSTRAINT `Listens_ibfk_2` FOREIGN KEY (`song_id`) REFERENCES `Song` (`song_id`) ON DELETE CASCADE
);

DROP TABLE IF EXISTS `Mood`;
CREATE TABLE `Mood` (
  `mood_id` int NOT NULL AUTO_INCREMENT,
  `mood_name` varchar(255) NOT NULL,
  PRIMARY KEY (`mood_id`)
);

DROP TABLE IF EXISTS `Playlist`;
CREATE TABLE `Playlist` (
  `playlist_id` int NOT NULL AUTO_INCREMENT,
  `playlist_name` varchar(255) NOT NULL,
  `creator_id` varchar(255) NOT NULL,
  PRIMARY KEY (`playlist_id`),
  KEY `creator_id` (`creator_id`),
  CONSTRAINT `Playlist_ibfk_1` FOREIGN KEY (`creator_id`) REFERENCES `User` (`user_id`) ON DELETE CASCADE
);

DROP TABLE IF EXISTS `Playlist_Collaborators`;
CREATE TABLE `Playlist_Collaborators` (
  `playlist_id` int NOT NULL,
  `collaborator_id` varchar(255) NOT NULL,
  PRIMARY KEY (`playlist_id`,`collaborator_id`),
  KEY `collaborator_id` (`collaborator_id`),
  CONSTRAINT `Playlist_Collaborators_ibfk_1` FOREIGN KEY (`playlist_id`) REFERENCES `Playlist` (`playlist_id`) ON DELETE CASCADE,
  CONSTRAINT `Playlist_Collaborators_ibfk_2` FOREIGN KEY (`collaborator_id`) REFERENCES `User` (`user_id`) ON DELETE CASCADE
);

DROP TABLE IF EXISTS `Playlist_Songs`;
CREATE TABLE `Playlist_Songs` (
  `playlist_id` int NOT NULL,
  `song_id` int NOT NULL,
  PRIMARY KEY (`playlist_id`,`song_id`),
  KEY `song_id` (`song_id`),
  CONSTRAINT `Playlist_Songs_ibfk_1` FOREIGN KEY (`playlist_id`) REFERENCES `Playlist` (`playlist_id`) ON DELETE CASCADE,
  CONSTRAINT `Playlist_Songs_ibfk_2` FOREIGN KEY (`song_id`) REFERENCES `Song` (`song_id`) ON DELETE CASCADE
);

DROP TABLE IF EXISTS `Pref_Artist`;
CREATE TABLE `Pref_Artist` (
  `user_id` varchar(255) NOT NULL,
  `artist_id` int NOT NULL,
  `artist_points` int NOT NULL,
  PRIMARY KEY (`user_id`,`artist_id`),
  KEY `artist_id` (`artist_id`),
  CONSTRAINT `Pref_Artist_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `User` (`user_id`) ON DELETE CASCADE,
  CONSTRAINT `Pref_Artist_ibfk_2` FOREIGN KEY (`artist_id`) REFERENCES `Artist` (`artist_id`) ON DELETE CASCADE
);

DROP TABLE IF EXISTS `Pref_Genre`;
CREATE TABLE `Pref_Genre` (
  `user_id` varchar(255) NOT NULL,
  `genre_id` int NOT NULL,
  `genre_points` int NOT NULL,
  PRIMARY KEY (`user_id`,`genre_id`),
  KEY `genre_id` (`genre_id`),
  CONSTRAINT `Pref_Genre_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `User` (`user_id`) ON DELETE CASCADE,
  CONSTRAINT `Pref_Genre_ibfk_2` FOREIGN KEY (`genre_id`) REFERENCES `Genre` (`genre_id`) ON DELETE CASCADE
);

DROP TABLE IF EXISTS `Pref_Mood`;
CREATE TABLE `Pref_Mood` (
  `user_id` varchar(255) NOT NULL,
  `mood_id` int NOT NULL,
  `mood_points` int NOT NULL,
  PRIMARY KEY (`user_id`,`mood_id`),
  KEY `mood_id` (`mood_id`),
  CONSTRAINT `Pref_Mood_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `User` (`user_id`) ON DELETE CASCADE,
  CONSTRAINT `Pref_Mood_ibfk_2` FOREIGN KEY (`mood_id`) REFERENCES `Mood` (`mood_id`) ON DELETE CASCADE
);

DROP TABLE IF EXISTS `Song`;
CREATE TABLE `Song` (
  `song_id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `release_date` datetime NOT NULL,
  `artist_id` int NOT NULL,
  `genre_id` int NOT NULL,
  `mood_id` int NOT NULL,
  PRIMARY KEY (`song_id`),
  KEY `artist_id` (`artist_id`),
  KEY `genre_id` (`genre_id`),
  KEY `mood_id` (`mood_id`),
  CONSTRAINT `Song_ibfk_1` FOREIGN KEY (`artist_id`) REFERENCES `Artist` (`artist_id`) ON DELETE CASCADE,
  CONSTRAINT `Song_ibfk_2` FOREIGN KEY (`genre_id`) REFERENCES `Genre` (`genre_id`) ON DELETE CASCADE,
  CONSTRAINT `Song_ibfk_3` FOREIGN KEY (`mood_id`) REFERENCES `Mood` (`mood_id`) ON DELETE CASCADE
);

DROP TABLE IF EXISTS `User`;
CREATE TABLE `User` (
  `user_id` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `first_name` varchar(255) NOT NULL,
  `last_name` varchar(255) DEFAULT NULL,
  `picture` blob,
  `phone_number` varchar(255) DEFAULT NULL,
  `premium` tinyint DEFAULT NULL,
  PRIMARY KEY (`user_id`)
);

DROP TRIGGER IF EXISTS `Before_Insert_Playlist_Songs`;
DELIMITER //
CREATE TRIGGER Before_Insert_Playlist_Songs
BEFORE INSERT ON Playlist_Songs FOR EACH ROW
BEGIN
    -- Declare variables
    DECLARE user_premium_status INT;
    DECLARE playlist_song_count INT;

    -- Fetch user premium status
    SELECT premium INTO user_premium_status
    FROM User
    WHERE user_id = (SELECT creator_id FROM Playlist WHERE playlist_id = NEW.playlist_id);

    -- Check if the user is a premium user
    IF user_premium_status IS NULL OR user_premium_status = 0 THEN
        -- Regular user, limit to 20 songs
        SELECT COUNT(*) INTO playlist_song_count
        FROM Playlist_Songs
        WHERE playlist_id = NEW.playlist_id;

        IF playlist_song_count + 1 > 20 THEN
            -- Throw an error if the limit is exceeded
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Regular users can add a maximum of 20 songs to a playlist.';
        END IF;
    END IF;
    -- Premium user, no limit on the number of songs
END //
DELIMITER ;

DROP PROCEDURE IF EXISTS `GetSongRecommendations`;
DELIMITER //
CREATE PROCEDURE GetSongRecommendations(IN p_user_id VARCHAR(255), IN num_songs INT)
BEGIN
    -- Declare variables
    DECLARE done BOOLEAN DEFAULT FALSE;
    DECLARE cur_song_id INT;
    DECLARE cur_score DECIMAL(5, 2);
    DECLARE user_genre_points INT;
    DECLARE user_mood_points INT;
    DECLARE user_artist_points INT;

    -- Declare cursor
    DECLARE song_cursor CURSOR FOR
        SELECT s.song_id,
               (
                   user_genre_points * COALESCE(pg.genre_points, 0) +
                   user_mood_points * COALESCE(pm.mood_points, 0) +
                   user_artist_points * COALESCE(pa.artist_points, 0)
               ) AS score
        FROM Song s
        LEFT JOIN Pref_Genre pg ON s.genre_id = pg.genre_id AND pg.user_id = p_user_id
        LEFT JOIN Pref_Mood pm ON s.mood_id = pm.mood_id AND pm.user_id = p_user_id
        LEFT JOIN Pref_Artist pa ON s.artist_id = pa.artist_id AND pa.user_id = p_user_id
        WHERE s.song_id NOT IN (SELECT song_id FROM Listens WHERE listener_id = p_user_id)
        ORDER BY score DESC
        LIMIT num_songs;

     -- Declare continue handler for the cursor
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    -- Fetch user preference points
    SELECT COALESCE(SUM(pg.genre_points), 0) INTO user_genre_points
    FROM Pref_Genre pg
    WHERE pg.user_id = p_user_id;

    SELECT COALESCE(SUM(pm.mood_points), 0) INTO user_mood_points
    FROM Pref_Mood pm
    WHERE pm.user_id = p_user_id;

    SELECT COALESCE(SUM(pa.artist_points), 0) INTO user_artist_points
    FROM Pref_Artist pa
    WHERE pa.user_id = p_user_id;

    -- Create temporary table to store recommended songs
    CREATE TEMPORARY TABLE RecommendedSongs (
        song_id INT,
        recommendation_score DECIMAL(5, 2)
    );

    -- Open the cursor
    OPEN song_cursor;

    -- Loop to fetch data from the cursor
    song_loop: LOOP
        -- Fetch data into variables
        FETCH song_cursor INTO cur_song_id, cur_score;

        -- Check if done fetching
        IF done THEN
            LEAVE song_loop;
        END IF;

        -- Insert into temporary table
        INSERT INTO RecommendedSongs (song_id, recommendation_score)
        VALUES (cur_song_id, cur_score);
    END LOOP;

    -- Close the cursor
    CLOSE song_cursor;

    -- Select and display recommended songs
    SELECT rs.song_id, s.title, s.artist_id, a.artist_name, s.genre_id, g.genre_name, s.mood_id, m.mood_name
    FROM RecommendedSongs rs
    INNER JOIN Song s ON rs.song_id = s.song_id
    INNER JOIN Artist a ON s.artist_id = a.artist_id
    INNER JOIN Genre g ON s.genre_id = g.genre_id
    INNER JOIN Mood m ON s.mood_id = m.mood_id;

    -- Drop the temporary table
    DROP TEMPORARY TABLE IF EXISTS RecommendedSongs;
END //
DELIMITER ;

