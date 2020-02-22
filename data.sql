-- phpMyAdmin SQL Dump
-- version 4.8.5
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Feb 22, 2020 at 05:24 PM
-- Server version: 5.7.26
-- PHP Version: 7.2.18

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `asm`
--

-- --------------------------------------------------------

--
-- Table structure for table `data`
--

DROP TABLE IF EXISTS `data`;
CREATE TABLE IF NOT EXISTS `data` (
  `id` varchar(30) NOT NULL,
  `cgpa` varchar(30) NOT NULL,
  `personalData` longtext NOT NULL,
  `marksData` longtext NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Dumping data for table `data`
--

INSERT INTO `data` (`id`, `cgpa`, `personalData`, `marksData`) VALUES
('17BK1A05A8138716', '7.25', '{\'HTNO:\': \'17BK1A05A8\', \'NAME:\': \'RAGULA SAI TEJA\', \'FATHER NAME:\': \'RAGULA THIRUPATHI\', \'COLLEGE CODE:\': \'BK\'}', '{\'COMPUTER NETWORKS LAB \': \'O\', \'DESIGN AND ANALYSIS OF ALGORITHMS LAB \': \'A+\', \'SOFTWARE ENGINEERING LAB \': \'O\', \'PROFESSIONAL ETHICS\': \'A\', \'DATA COMMUNICATION AND COMPUTER NETWORKS \': \'B+\', \'DESIGN AND ANALYSIS OF ALGORITHMS\': \'B+\', \'FUNDAMENTALS OF MANAGEMENT\': \'B\', \'SOFTWARE ENGINEERING\': \'B\', \'PRINCIPLES OF ELECTRONIC COMMUNICATIONS\': \'B\'}');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
