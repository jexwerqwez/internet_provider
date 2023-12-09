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
-- Table structure for table `all_services`
--

DROP TABLE IF EXISTS `all_services`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `all_services` (
  `all_services_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(90) NOT NULL,
  `cost` int NOT NULL,
  `description` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`all_services_id`)
) ENGINE=InnoDB AUTO_INCREMENT=667 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `all_services`
--

LOCK TABLES `all_services` WRITE;
/*!40000 ALTER TABLE `all_services` DISABLE KEYS */;
INSERT INTO `all_services` VALUES (101,'Интернет 100 Мбит/c',400,'Скорость интернета до 100 Мбит/c'),(102,'Интернет 200 Мбит/c',500,'Скорость интернета до 200 Мбит/c'),(103,'Интернет 50 Мбит/с',300,'Скорость интернета до 50 Мбит/c'),(104,'Интернет 25 Мбит/с',200,'Скорость интернета до 25 Мбит/c'),(202,'Цифровое телевидение',160,'200 каналов'),(303,'Онлайн-кинотеатр',299,'100 000 фильмов и сериалов'),(401,'Аренда роутера',100,'Гигабитный роутер с гарантией 2 года'),(404,'Аренда тарелки',144,'Полный комплект с ТВ-приставкой и антенной'),(666,'Подписка на антивирусник',89,'Защита от лучшего антивирусника MicroOleg');
/*!40000 ALTER TABLE `all_services` ENABLE KEYS */;
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
