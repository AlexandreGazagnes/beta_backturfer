/*!40000 ALTER TABLE `cachedate` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `caractrap`
--

DROP TABLE IF EXISTS `caractrap`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `caractrap` (
  `id` bigint(11) NOT NULL AUTO_INCREMENT,
  `comp` int(11) NOT NULL,
  `jour` varchar(255) DEFAULT NULL,
  `heure` time DEFAULT NULL,
  `hippo` varchar(255) DEFAULT NULL,
  `reun` varchar(255) DEFAULT NULL,
  `prix` double DEFAULT NULL,
  `prixnom` varchar(255) DEFAULT NULL,
  `meteo` varchar(255) DEFAULT NULL,
  `typec` varchar(255) DEFAULT NULL,
  `partant` varchar(255) DEFAULT NULL,
  `handi` varchar(255) DEFAULT NULL,
  `reclam` varchar(255) DEFAULT NULL,
  `dist` varchar(255) DEFAULT NULL,
  `groupe` varchar(255) DEFAULT NULL,
  `sex` varchar(255) DEFAULT NULL,
  `corde` varchar(255) DEFAULT NULL,
  `age` varchar(255) DEFAULT NULL,
  `autos` varchar(255) DEFAULT NULL,
  `cheque` varchar(255) DEFAULT NULL,
  `europ` varchar(255) DEFAULT NULL,
  `quinte` double DEFAULT NULL,
  `natpis` varchar(255) DEFAULT NULL,
  `amat` varchar(255) DEFAULT NULL,
  `courseabc` varchar(255) DEFAULT NULL,
  `pistegp` varchar(255) DEFAULT NULL,
  `arriv` varchar(255) DEFAULT NULL,
  `lice` varchar(255) DEFAULT NULL,
  `temperature` int(11) DEFAULT NULL,
  `forceVent` int(11) DEFAULT NULL,
  `directionVent` varchar(6) NOT NULL,
  `nebulositeLibelleCourt` text NOT NULL,
  `condi` varchar(255) DEFAULT NULL,
  `url` text NOT NULL,
  `tempscourse` text NOT NULL,
  `updatedAt` timestamp NULL DEFAULT NULL,
  `createdAt` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2283293158 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `caractrap`
--

LOCK TABLES `caractrap` WRITE;
/*!40000 ALTER TABLE `caractrap` DISABLE KEYS */;
