-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Oct 20, 2023 at 06:31 AM
-- Server version: 10.4.27-MariaDB
-- PHP Version: 8.2.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `game4d`
--

-- --------------------------------------------------------

--
-- Table structure for table `4dtoto`
--

CREATE TABLE `4dtoto` (
  `batch` varchar(96) NOT NULL,
  `totoid` varchar(90) NOT NULL,
  `40toto_number` int(4) NOT NULL,
  `username` varchar(96) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `toto_prize_pool`
--

CREATE TABLE `toto_prize_pool` (
  `4d_batch` varchar(96) NOT NULL,
  `first` int(11) NOT NULL,
  `second` int(11) NOT NULL,
  `third` int(11) NOT NULL,
  `starter` int(11) NOT NULL,
  `consolation` int(11) NOT NULL,
  `accumulate_reward` int(20) NOT NULL,
  `timestamp` int(20) NOT NULL DEFAULT current_timestamp(),
  `status` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Triggers `toto_prize_pool`
--
DELIMITER $$
CREATE TRIGGER `4dtoto_batch` BEFORE INSERT ON `toto_prize_pool` FOR EACH ROW BEGIN
    DECLARE next_id INT;
    SELECT (SUBSTRING(MAX(4d_batch), 6) + 1) INTO next_id FROM 4dtoto_pool;
    
    IF next_id IS NULL THEN
        SET next_id = 1;
    END IF;

    WHILE (SELECT COUNT(*) FROM 4dtoto_pool WHERE 4d_batch = CONCAT('4DTOTO-', LPAD(next_id, 5, '0'))) > 0 DO
        SET next_id = next_id + 1;
    END WHILE;
    
    SET NEW.4d_batch = CONCAT('4DTOTO-', LPAD(next_id, 5, '0'));
END
$$
DELIMITER ;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `4dtoto`
--
ALTER TABLE `4dtoto`
  ADD PRIMARY KEY (`batch`,`totoid`);

--
-- Indexes for table `toto_prize_pool`
--
ALTER TABLE `toto_prize_pool`
  ADD PRIMARY KEY (`4d_batch`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
