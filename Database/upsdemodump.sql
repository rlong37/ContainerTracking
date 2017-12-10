-- MySQL dump 10.15  Distrib 10.0.31-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: upsdemo
-- ------------------------------------------------------
-- Server version	10.0.31-MariaDB-0ubuntu0.16.04.2

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `CAMERA_LOCATIONS`
--

DROP TABLE IF EXISTS `CAMERA_LOCATIONS`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `CAMERA_LOCATIONS` (
  `CAMERA_ID` varchar(100) COLLATE utf8_bin NOT NULL,
  `LOCATION` varchar(100) COLLATE utf8_bin NOT NULL,
  PRIMARY KEY (`CAMERA_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `CAMERA_LOCATIONS`
--

LOCK TABLES `CAMERA_LOCATIONS` WRITE;
/*!40000 ALTER TABLE `CAMERA_LOCATIONS` DISABLE KEYS */;
INSERT INTO `CAMERA_LOCATIONS` VALUES ('testCam','Not Scanned');
/*!40000 ALTER TABLE `CAMERA_LOCATIONS` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `CONTAINERS`
--

DROP TABLE IF EXISTS `CONTAINERS`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `CONTAINERS` (
  `ID` varchar(100) COLLATE utf8_bin NOT NULL,
  `FRAGILE` tinyint(1) NOT NULL DEFAULT '0',
  `PRIORITY` int(11) NOT NULL,
  `CONTENT` int(11) NOT NULL,
  `CAMERA_ID` varchar(100) COLLATE utf8_bin NOT NULL DEFAULT '0',
  PRIMARY KEY (`ID`),
  KEY `CONTAINERS_PRIORITIES_FK` (`PRIORITY`),
  KEY `CONTAINERS_Contents_FK` (`CONTENT`),
  KEY `CONTAINERS_CAMERA_LOCATIONS_FK` (`CAMERA_ID`),
  CONSTRAINT `CONTAINERS_CAMERA_LOCATIONS_FK` FOREIGN KEY (`CAMERA_ID`) REFERENCES `CAMERA_LOCATIONS` (`CAMERA_ID`),
  CONSTRAINT `CONTAINERS_Contents_FK` FOREIGN KEY (`CONTENT`) REFERENCES `Contents` (`ID`),
  CONSTRAINT `CONTAINERS_PRIORITIES_FK` FOREIGN KEY (`PRIORITY`) REFERENCES `PRIORITIES` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `CONTAINERS`
--

LOCK TABLES `CONTAINERS` WRITE;
/*!40000 ALTER TABLE `CONTAINERS` DISABLE KEYS */;
INSERT INTO `CONTAINERS` VALUES ('AAD6598UP',0,4,1,'testCam'),('AAZ23864UPS',0,2,3,'testCam'),('FJA57283UPS',1,3,4,'testCam');
/*!40000 ALTER TABLE `CONTAINERS` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Contents`
--

DROP TABLE IF EXISTS `Contents`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Contents` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Type` varchar(100) COLLATE utf8_bin NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Contents`
--

LOCK TABLES `Contents` WRITE;
/*!40000 ALTER TABLE `Contents` DISABLE KEYS */;
INSERT INTO `Contents` VALUES (1,'Medical'),(2,'Chemical'),(3,'Food'),(4,'Electronic'),(5,'Industrial');
/*!40000 ALTER TABLE `Contents` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `PRIORITIES`
--

DROP TABLE IF EXISTS `PRIORITIES`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `PRIORITIES` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `PRIORITY` varchar(100) COLLATE utf8_bin NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `PRIORITIES`
--

LOCK TABLES `PRIORITIES` WRITE;
/*!40000 ALTER TABLE `PRIORITIES` DISABLE KEYS */;
INSERT INTO `PRIORITIES` VALUES (1,'New'),(2,'High Priority'),(3,'Low Priority'),(4,'Part of large order');
/*!40000 ALTER TABLE `PRIORITIES` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-12-09  9:41:53
