-- phpMyAdmin SQL Dump
-- version 5.0.2
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1:3306
-- Généré le : jeu. 03 juin 2021 à 08:08
-- Version du serveur :  5.7.31
-- Version de PHP : 7.3.21

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

DROP DATABASE IF EXISTS artefakt_ai;
CREATE DATABASE artefakt_ai;
USE artefakt_ai;

-- --------------------------------------------------------

--
-- Structure de la table `customer`
--

DROP TABLE IF EXISTS `customer`;
CREATE TABLE IF NOT EXISTS `customer` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `first_name` varchar(100) COLLATE utf8_bin NOT NULL,
  `last_name` varchar(100) COLLATE utf8_bin NOT NULL,
  `email` varchar(255) COLLATE utf8_bin NOT NULL,
  `password` varchar(100) COLLATE utf8_bin DEFAULT NULL,
  `organization` varchar(255) COLLATE utf8_bin DEFAULT NULL,
  `specialization_id` int(11) DEFAULT NULL,
  `organization_type_id` int(11) DEFAULT NULL,
  `pm_system_id` int(11) DEFAULT NULL,
  `gender_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_CUSTOMER_specialization_id` (`specialization_id`),
  KEY `fk_CUSTOMER_organization_type_id` (`organization_type_id`),
  KEY `fk_CUSTOMER_pm_system_id` (`pm_system_id`),
  KEY `fk_CUSTOMER_gender_id` (`gender_id`)
) ENGINE=MyISAM AUTO_INCREMENT=14 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- --------------------------------------------------------

--
-- Structure de la table `gender`
--

DROP TABLE IF EXISTS `gender`;
CREATE TABLE IF NOT EXISTS `gender` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` enum('Male','Female','Other') COLLATE utf8_bin NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

--
-- Déchargement des données de la table `gender`
--

INSERT INTO `gender` (`id`, `name`) VALUES
(1, 'Male'),
(2, 'Female'),
(3, 'Other');

-- --------------------------------------------------------

--
-- Structure de la table `organization_type`
--

DROP TABLE IF EXISTS `organization_type`;
CREATE TABLE IF NOT EXISTS `organization_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type` enum('Choose Variant','Private Practice','Emerging DSO (3-9)','Mid-Market DSO (10-74)','Elite DSO (75+)','Insurer','University/Dental school/Hospital','Government Agency','Industry Partner','Other') COLLATE utf8_bin NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=11 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

--
-- Déchargement des données de la table `organization_type`
--

INSERT INTO `organization_type` (`id`, `type`) VALUES
(1, 'Choose Variant'),
(2, 'Private Practice'),
(3, 'Emerging DSO (3-9)'),
(4, 'Mid-Market DSO (10-74)'),
(5, 'Elite DSO (75+)'),
(6, 'Insurer'),
(7, 'University/Dental school/Hospital'),
(8, 'Government Agency'),
(9, 'Industry Partner'),
(10, 'Other');

-- --------------------------------------------------------

--
-- Structure de la table `pm_system`
--

DROP TABLE IF EXISTS `pm_system`;
CREATE TABLE IF NOT EXISTS `pm_system` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` enum('Choose variant','Dentrix 6-7','EagleSoft','Dentrix Ascent','Denticon','Carestack','Epic Wisdom','Other') COLLATE utf8_bin NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=9 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

--
-- Déchargement des données de la table `pm_system`
--

INSERT INTO `pm_system` (`id`, `name`) VALUES
(1, 'Choose variant'),
(2, 'Dentrix 6-7'),
(3, 'EagleSoft'),
(4, 'Dentrix Ascent'),
(5, 'Denticon'),
(6, 'Carestack'),
(7, 'Epic Wisdom'),
(8, 'Other');

-- --------------------------------------------------------

--
-- Structure de la table `posts`
--

DROP TABLE IF EXISTS `posts`;
CREATE TABLE IF NOT EXISTS `posts` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` text COLLATE utf8_bin NOT NULL,
  `content` text COLLATE utf8_bin NOT NULL,
  `customer_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_POST_customer_id` (`customer_id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- --------------------------------------------------------

--
-- Structure de la table `specialization`
--

DROP TABLE IF EXISTS `specialization`;
CREATE TABLE IF NOT EXISTS `specialization` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` enum('Choose variant','Manager','Dentist','Hygienist','Radiologist','Other') COLLATE utf8_bin NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=7 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

--
-- Déchargement des données de la table `specialization`
--

INSERT INTO `specialization` (`id`, `name`) VALUES
(1, 'Choose variant'),
(2, 'Manager'),
(3, 'Dentist'),
(4, 'Hygienist'),
(5, 'Radiologist'),
(6, 'Other');

-- --------------------------------------------------------

--
-- Structure de la table `x_ray`
--

DROP TABLE IF EXISTS `x_ray`;
CREATE TABLE IF NOT EXISTS `x_ray` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `link` text COLLATE utf8_bin NOT NULL,
  `customer_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_X_RAY_customer_id` (`customer_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- --------------------------------------------------------

--
-- Structure de la table `x_ray_segmentation`
--

DROP TABLE IF EXISTS `x_ray_segmentation`;
CREATE TABLE IF NOT EXISTS `x_ray_segmentation` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `link` text COLLATE utf8_bin NOT NULL,
  `x_ray_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_X_RAY_SEGMENTATION_x_ray_id` (`x_ray_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

DROP USER IF EXISTS 'util_artefakt'@'localhost';
CREATE USER 'util_artefakt'@'localhost' IDENTIFIED BY 'artefakt';
GRANT USAGE ON *.* TO 'util_artefakt'@'localhost' REQUIRE NONE WITH MAX_QUERIES_PER_HOUR 0 MAX_CONNECTIONS_PER_HOUR 0 MAX_UPDATES_PER_HOUR 0 MAX_USER_CONNECTIONS 0;
GRANT ALL PRIVILEGES ON `artefakt_ai`.* TO 'util_artefakt'@'localhost' WITH GRANT OPTION;
