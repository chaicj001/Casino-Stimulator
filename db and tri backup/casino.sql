-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 24, 2023 at 02:40 PM
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
-- Database: `casino`
--

-- --------------------------------------------------------

--
-- Table structure for table `slot_machine_history`
--

CREATE TABLE `slot_machine_history` (
  `sm_id` varchar(96) NOT NULL,
  `username` varchar(96) NOT NULL,
  `bet_amount` decimal(9,2) NOT NULL,
  `winnings` varchar(96) NOT NULL,
  `symbols` varchar(96) NOT NULL,
  `spin_time` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `slot_machine_history`
--

INSERT INTO `slot_machine_history` (`sm_id`, `username`, `bet_amount`, `winnings`, `symbols`, `spin_time`) VALUES
('', 'admin', '1000.00', '0', 'snake,dog,monkey', '2023-05-24 18:05:16'),
('', 'admin', '10000.00', '0', 'chicken,rat,rabbit', '2023-05-24 18:05:26'),
('', 'admin', '1000.00', '0', 'cow,horse,monkey', '2023-05-24 18:13:23'),
('', 'admin', '1000.00', '0', 'monkey,horse,tiger', '2023-05-24 18:13:31'),
('', 'admin', '1000.00', '0', 'rabbit,monkey,tiger', '2023-05-24 18:13:35'),
('', 'admin', '1000.00', '0', 'chicken,snake,dragon', '2023-05-24 18:13:39'),
('', 'admin', '1000.00', '0', 'pig,goat,monkey', '2023-05-24 18:13:42'),
('', 'admin', '1000.00', '0', 'rabbit,snake,dragon', '2023-05-24 18:14:35'),
('', 'admin', '100.00', '0', 'dragon,snake,goat', '2023-05-24 18:14:47'),
('', 'admin', '100.00', '0', 'tiger,dog,dog', '2023-05-24 18:14:49'),
('', 'admin', '100.00', '0', 'pig,chicken,snake', '2023-05-24 18:14:50'),
('', 'admin', '100.00', '0', 'tiger,dragon,rat', '2023-05-24 18:14:52'),
('', 'admin', '100.00', '0', 'dog,chicken,monkey', '2023-05-24 18:14:54'),
('', 'admin', '1000.00', '0', 'dragon,snake,pig', '2023-05-24 18:21:42');

--
-- Triggers `slot_machine_history`
--
DELIMITER $$
CREATE TRIGGER `slotmachineid_tri` BEFORE INSERT ON `slot_machine_history` FOR EACH ROW BEGIN
    DECLARE next_id VARCHAR(10);
    SELECT CONCAT('SM-', LPAD((SUBSTRING(MAX(slot_machine_id), 4) + 1), 3, '0')) INTO next_id FROM slot_machine_history;
    IF next_id IS NULL THEN
        SET next_id = 'SM-001';
    END IF;
    SET NEW.sm_id = next_id;
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `topup_history`
--

CREATE TABLE `topup_history` (
  `topup_id` varchar(96) NOT NULL,
  `username` varchar(96) NOT NULL,
  `bef_topup` decimal(9,2) NOT NULL,
  `after_topup` decimal(9,2) NOT NULL,
  `topup_amt` decimal(9,2) NOT NULL,
  `topup_time` datetime NOT NULL,
  `user_topup` varchar(96) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `topup_history`
--

INSERT INTO `topup_history` (`topup_id`, `username`, `bef_topup`, `after_topup`, `topup_amt`, `topup_time`, `user_topup`) VALUES
('', 'user1', '1000.00', '2000.00', '1000.00', '2023-05-24 17:29:31', ''),
('', 'admin', '100100.00', '100200.00', '100.00', '2023-05-24 17:30:53', 'admin'),
('', 'user1', '2000.00', '2100.00', '100.00', '2023-05-24 17:31:16', 'admin');

--
-- Triggers `topup_history`
--
DELIMITER $$
CREATE TRIGGER `topupid_tri` BEFORE INSERT ON `topup_history` FOR EACH ROW BEGIN
    DECLARE next_id VARCHAR(10);
    SELECT CONCAT('TP-', LPAD((SUBSTRING(MAX(topup_id), 4) + 1), 3, '0')) INTO next_id FROM topup_history;
    IF next_id IS NULL THEN
        SET next_id = 'TP-001';
    END IF;
    SET NEW.topup_id = next_id;
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `priv` varchar(20) NOT NULL DEFAULT '''user''',
  `balance` decimal(10,2) NOT NULL DEFAULT 0.00,
  `last_login` datetime DEFAULT NULL,
  `last_logout` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`username`, `password`, `priv`, `balance`, `last_login`, `last_logout`) VALUES
('admin', 'admin', 'admin', '77900.00', '2023-05-24 20:36:22', '2023-05-24 18:28:49'),
('banker', 'banker', 'banker', '119500.00', NULL, NULL),
('user1', 'user1', 'user', '2100.00', '2023-05-24 20:36:13', '2023-05-24 20:36:19');

-- --------------------------------------------------------

--
-- Table structure for table `winloss_history`
--

CREATE TABLE `winloss_history` (
  `winloss_id` varchar(96) NOT NULL,
  `username` varchar(96) NOT NULL,
  `bet_amount` int(90) NOT NULL,
  `result` varchar(96) NOT NULL,
  `createtime` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `winloss_history`
--

INSERT INTO `winloss_history` (`winloss_id`, `username`, `bet_amount`, `result`, `createtime`) VALUES
('', 'admin', 100, 'win', '2023-05-24 18:37:35'),
('', 'admin', 11, 'win', '2023-05-24 18:37:41'),
('', 'admin', 22, 'win', '2023-05-24 18:37:44'),
('', 'admin', 33, 'loss', '2023-05-24 18:37:46'),
('', 'admin', 33, 'loss', '2023-05-24 18:37:47'),
('WL-001', 'admin', 20000, 'loss', '2023-05-24 20:36:32'),
('WL-002', 'admin', 1000, 'win', '2023-05-24 20:39:37'),
('WL-003', 'admin', 1000, 'loss', '2023-05-24 20:39:40'),
('WL-004', 'admin', 1000, 'loss', '2023-05-24 20:40:01');

--
-- Triggers `winloss_history`
--
DELIMITER $$
CREATE TRIGGER `winlossid_tri` BEFORE INSERT ON `winloss_history` FOR EACH ROW BEGIN    
    DECLARE next_id VARCHAR(10);
    SELECT CONCAT('WL-', LPAD((SUBSTRING(MAX(winloss_id), 4) + 1), 3, '0')) INTO next_id FROM winloss_history;
    IF next_id IS NULL THEN
        SET next_id = 'WL-001';
    END IF;
    SET NEW.winloss_id = next_id;
END
$$
DELIMITER ;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`username`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
