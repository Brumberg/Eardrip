-- MySQL dump 10.13  Distrib 8.0.28, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: eardrip_users
-- ------------------------------------------------------
-- Server version	8.0.28

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `trackdata`
--

DROP TABLE IF EXISTS `trackdata`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `trackdata` (
  `field_track_id` varchar(250) DEFAULT NULL,
  `field_artist_id` varchar(250) DEFAULT NULL,
  `field_title_id` varchar(250) DEFAULT NULL,
  `field_genre_id` varchar(250) DEFAULT NULL,
  `field_popularity` varchar(250) DEFAULT NULL,
  `field_danceability` varchar(250) DEFAULT NULL,
  `field_energy` varchar(250) DEFAULT NULL,
  `field_key` varchar(250) DEFAULT NULL,
  `field_loudness` varchar(250) DEFAULT NULL,
  `field_mode` varchar(250) DEFAULT NULL,
  `field_speechiness` varchar(250) DEFAULT NULL,
  `field_acousticness` varchar(250) DEFAULT NULL,
  `field_instrumentalness` varchar(250) DEFAULT NULL,
  `field_liveness` varchar(250) DEFAULT NULL,
  `field_valence` varchar(250) DEFAULT NULL,
  `field_tempo` varchar(250) DEFAULT NULL,
  `field_type` varchar(250) DEFAULT NULL,
  `field_id` varchar(250) DEFAULT NULL,
  `field_uri` varchar(250) DEFAULT NULL,
  `field_track_href` varchar(250) DEFAULT NULL,
  `field_analysis_url` varchar(250) DEFAULT NULL,
  `field_duration_ms` varchar(250) DEFAULT NULL,
  `field_time_signature` varchar(250) DEFAULT NULL,
  `tlike` varchar(250) DEFAULT NULL,
  `userID` int DEFAULT NULL,
  KEY `userID` (`userID`),
  CONSTRAINT `userID` FOREIGN KEY (`userID`) REFERENCES `user` (`userID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `trackdata`
--

LOCK TABLES `trackdata` WRITE;
/*!40000 ALTER TABLE `trackdata` DISABLE KEYS */;
INSERT INTO `trackdata` VALUES ('5iyZwawawLjHYpX4MxUKVF','Ava Max','Salt','dance pop,pop','75','0.693','0.835','6','-3.242','1','0.0624','0.131','0','0.073','0.744','128.052','audio_features','5iyZwawawLjHYpX4MxUKVF','spotify:track:5iyZwawawLjHYpX4MxUKVF','https://api.spotify.com/v1/tracks/5iyZwawawLjHYpX4MxUKVF','https://api.spotify.com/v1/audio-analysis/5iyZwawawLjHYpX4MxUKVF','180283','4','tlike',1),('7kQUdVjev73xIuwu7W6YW9','SR','Welcome To Brixton','uk drill','80','0.89','0.455','2','-10.226','1','0.437','0.158','0','0.153','0.897','138.988','audio_features','7kQUdVjev73xIuwu7W6YW9','spotify:track:7kQUdVjev73xIuwu7W6YW9','https://api.spotify.com/v1/tracks/7kQUdVjev73xIuwu7W6YW9','https://api.spotify.com/v1/audio-analysis/7kQUdVjev73xIuwu7W6YW9','180000','4','tlike',1),('09VwLfTaX6fYDZhofvEVbw','SR','Brucky','uk drill','58','0.873','0.652','5','-11.783','0','0.467','0.361','2.81e-05','0.182','0.682','151.862','audio_features','09VwLfTaX6fYDZhofvEVbw','spotify:track:09VwLfTaX6fYDZhofvEVbw','https://api.spotify.com/v1/tracks/09VwLfTaX6fYDZhofvEVbw','https://api.spotify.com/v1/audio-analysis/09VwLfTaX6fYDZhofvEVbw','213158','4','tlike',1);
/*!40000 ALTER TABLE `trackdata` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-02-15 23:17:34
