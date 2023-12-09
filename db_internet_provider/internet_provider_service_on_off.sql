-- MySQL dump 10.13  Distrib 8.0.32, for Win64 (x86_64)
--
-- Host: localhost    Database: internet_provider
-- ------------------------------------------------------
-- Server version	8.0.32

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
-- Table structure for table `service_on_off`
--

DROP TABLE IF EXISTS `service_on_off`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `service_on_off` (
  `service_on_off_id` int NOT NULL AUTO_INCREMENT,
  `on_date` datetime NOT NULL,
  `off_date` datetime DEFAULT NULL,
  `contract_number` bigint DEFAULT NULL,
  `all_services_id` int DEFAULT NULL,
  PRIMARY KEY (`service_on_off_id`),
  KEY `contract_id_service_idx` (`contract_number`),
  KEY `all_services_id_changes_idx` (`all_services_id`),
  CONSTRAINT `all_services_sc` FOREIGN KEY (`all_services_id`) REFERENCES `all_services` (`all_services_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `contract_id_service` FOREIGN KEY (`contract_number`) REFERENCES `contract` (`contract_number`)
) ENGINE=InnoDB AUTO_INCREMENT=1113 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `service_on_off`
--

LOCK TABLES `service_on_off` WRITE;
/*!40000 ALTER TABLE `service_on_off` DISABLE KEYS */;
INSERT INTO `service_on_off` VALUES (1,'1980-02-20 00:00:00',NULL,111,101),(2,'2020-03-03 00:00:00','2022-01-02 00:00:00',831,101),(3,'2003-12-31 00:00:00',NULL,534,101),(4,'2002-07-07 00:00:00',NULL,534,303),(5,'2003-04-23 00:00:00','2013-01-15 00:00:00',678,101),(6,'2023-02-14 00:00:00',NULL,916,202),(7,'2020-03-17 00:00:00','2020-07-12 00:00:00',831,303),(8,'1999-01-10 00:00:00',NULL,534,666);
/*!40000 ALTER TABLE `service_on_off` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-12-09  6:47:52
