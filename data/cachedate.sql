-- MySQL dump 10.16  Distrib 10.1.26-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: pturfcop
-- ------------------------------------------------------
-- Server version	10.1.26-MariaDB-0+deb9u1

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
-- Table structure for table `cachedate`
--

DROP TABLE IF EXISTS `cachedate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cachedate` (
  `id` bigint(11) NOT NULL AUTO_INCREMENT,
  `comp` int(11) NOT NULL,
  `jour` date NOT NULL,
  `hippo` tinytext NOT NULL,
  `numcourse` bigint(11) NOT NULL,
  `cl` tinytext NOT NULL,
  `dist` smallint(4) NOT NULL,
  `partant` int(11) NOT NULL,
  `typec` text NOT NULL,
  `cheque` text NOT NULL,
  `numero` decimal(2,0) NOT NULL,
  `cheval` text NOT NULL,
  `sexe` text NOT NULL,
  `age` int(11) NOT NULL,
  `cotedirect` decimal(5,2) NOT NULL,
  `coteprob` decimal(5,2) NOT NULL,
  `recence` int(11) NOT NULL,
  `ecurie` text NOT NULL,
  `distpoids` text NOT NULL,
  `ecar` text NOT NULL,
  `redkm` text NOT NULL,
  `redkmInt` int(11) NOT NULL,
  `handiecords` text NOT NULL,
  `corde` decimal(2,0) NOT NULL,
  `defoeil` text NOT NULL,
  `recul` tinyint(1) DEFAULT '0',
  `gains` text NOT NULL,
  `musiquept` text NOT NULL,
  `musiqueche` text NOT NULL,
  `m1` int(11) DEFAULT NULL,
  `m2` int(11) DEFAULT NULL,
  `m3` int(11) DEFAULT NULL,
  `m4` int(11) DEFAULT NULL,
  `m5` int(11) DEFAULT NULL,
  `m6` int(11) DEFAULT NULL,
  `jockey` text NOT NULL,
  `musiquejoc` text NOT NULL,
  `montesdujockeyjour` text NOT NULL,
  `couruejockeyjour` text NOT NULL,
  `victoirejockeyjour` text NOT NULL,
  `entraineur` text NOT NULL,
  `musiqueent` text NOT NULL,
  `monteentraineurjour` int(11) NOT NULL,
  `courueentraineurjour` int(11) NOT NULL,
  `victoireentraineurjour` int(11) NOT NULL,
  `coursescheval` int(11) NOT NULL,
  `victoirescheval` int(11) NOT NULL,
  `placescheval` int(11) NOT NULL,
  `coursesentraineur` int(11) NOT NULL,
  `victoiresentraineur` int(11) NOT NULL,
  `placeentraineur` int(11) NOT NULL,
  `coursesjockey` int(11) NOT NULL,
  `victoiresjockey` int(11) NOT NULL,
  `placejockey` int(11) NOT NULL,
  `dernierhippo` text,
  `dernierealloc` text,
  `derniernbpartants` text,
  `dernieredist` text,
  `derniereplace` text,
  `dernierecote` text,
  `dernierJoc` text,
  `dernierEnt` text,
  `dernierProp` text,
  `proprietaire` text NOT NULL,
  `nbcoursepropjour` int(11) NOT NULL,
  `europ` text NOT NULL,
  `amat` text NOT NULL,
  `arrive` text NOT NULL,
  `txrecl` text NOT NULL,
  `pays` text NOT NULL,
  `meteo` text NOT NULL,
  `lice` text NOT NULL,
  `natpis` text NOT NULL,
  `pistegp` text NOT NULL,
  `prix` text NOT NULL,
  `poidmont` text NOT NULL,
  `pourcVictJock` decimal(5,2) NOT NULL,
  `pourcPlaceJock` decimal(5,2) NOT NULL,
  `pourcVictCheval` decimal(5,2) NOT NULL,
  `pourcPlaceCheval` decimal(5,2) NOT NULL,
  `pourcVictEnt` decimal(5,2) NOT NULL,
  `pourcPlaceEnt` decimal(5,2) NOT NULL,
  `pourcVictEntHippo` decimal(5,2) NOT NULL,
  `pourcVictJockHippo` decimal(5,2) NOT NULL,
  `pourcPlaceEntHippo` decimal(5,2) NOT NULL,
  `pourcPlaceJockHippo` decimal(5,2) NOT NULL,
  `pourcVictChevalHippo` decimal(5,2) NOT NULL,
  `pourcPlaceChevalHippo` decimal(5,2) NOT NULL,
  `nbrCourseJockHippo` int(11) NOT NULL,
  `nbrCourseEntHippo` int(11) NOT NULL,
  `nbrCourseChevalHippo` int(11) NOT NULL,
  `nbCourseCouple` int(11) NOT NULL,
  `nbVictCouple` int(11) NOT NULL,
  `nbPlaceCouple` int(11) NOT NULL,
  `TxVictCouple` decimal(5,2) NOT NULL,
  `TxPlaceCouple` decimal(5,2) NOT NULL,
  `nbCourseCoupleHippo` int(11) NOT NULL,
  `nbVictCoupleHippo` int(11) NOT NULL,
  `nbPlaceCoupleHippo` int(11) NOT NULL,
  `TxVictCoupleHippo` decimal(5,2) NOT NULL,
  `TxPlaceCoupleHippo` decimal(5,2) NOT NULL,
  `pere` text NOT NULL,
  `mere` text NOT NULL,
  `peremere` text NOT NULL,
  `coteleturf` text NOT NULL,
  `commen` text NOT NULL,
  `gainsCarriere` int(11) NOT NULL,
  `gainsVictoires` int(11) NOT NULL,
  `gainsPlace` int(11) NOT NULL,
  `gainsAnneeEnCours` int(11) NOT NULL,
  `gainsAnneePrecedente` int(11) NOT NULL,
  `jumentPleine` tinyint(1) NOT NULL,
  `engagement` tinyint(1) NOT NULL,
  `handicapDistance` int(11) NOT NULL,
  `handicapPoids` int(11) NOT NULL,
  `indicateurInedit` tinyint(1) NOT NULL,
  `tempstot` text NOT NULL,
  `vha` text NOT NULL,
  `recordG` text,
  `txreclam` text NOT NULL,
  `createdat` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updatedat` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `rangTxVictJock` int(11) NOT NULL,
  `rangTxVictCheval` int(11) NOT NULL,
  `rangTxVictEnt` int(11) NOT NULL,
  `rangTxPlaceJock` int(11) NOT NULL,
  `rangTxPlaceCheval` int(11) NOT NULL,
  `rangTxPlaceEnt` int(11) NOT NULL,
  `rangRecordG` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `numcourse` (`numcourse`),
  KEY `jour` (`jour`),
  KEY `chejou` (`cheval`(10),`jour`),
  KEY `propjour` (`proprietaire`(10),`jour`),
  KEY `jourhippojoc` (`jour`,`hippo`(10),`jockey`(10)),
  KEY `jourhippoent` (`jour`,`hippo`(10),`entraineur`(10)),
  KEY `jourhippoche` (`jour`,`hippo`(10),`cheval`(10)),
  KEY `jocjou` (`jockey`(20),`jour`) USING BTREE,
  KEY `entjou` (`entraineur`(20),`jour`) USING BTREE,
  KEY `dist` (`dist`),
  KEY `comp` (`comp`)
) ENGINE=InnoDB AUTO_INCREMENT=228329113812 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cachedate`
--

LOCK TABLES `cachedate` WRITE;
/*!40000 ALTER TABLE `cachedate` DISABLE KEYS */;
