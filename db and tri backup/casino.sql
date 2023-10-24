-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Oct 20, 2023 at 06:30 AM
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
('SM-001', 'admin', '100.00', '2000.0', 'dragon,dragon,dragon', '2023-06-05 19:26:46'),
('SM-002', 'admin', '100.00', '2000.0', 'dragon,dragon,dragon', '2023-06-05 19:26:53'),
('SM-003', 'admin', '100.00', '2000.0', 'dragon,dragon,dragon', '2023-06-05 19:27:00'),
('SM-004', 'admin', '100.00', '2000.0', 'dragon,dragon,dragon', '2023-06-05 19:27:09'),
('SM-005', 'admin', '20.00', '400.0', 'dragon,dragon,dragon', '2023-06-06 00:33:34'),
('SM-006', 'admin', '100.00', '2000.0', 'dragon,dragon,dragon', '2023-06-15 17:04:08'),
('SM-007', 'admin', '100.00', '2000.0', 'dragon,dragon,dragon', '2023-06-15 17:04:12'),
('SM-008', 'admin', '100.00', '2000.0', 'dragon,dragon,dragon', '2023-06-15 17:04:14'),
('SM-009', 'admin', '100.00', '2000.0', 'dragon,dragon,dragon', '2023-06-15 17:49:59'),
('SM-010', 'admin', '100.00', '2000.0', 'dragon,dragon,dragon', '2023-06-15 17:50:06'),
('SM-011', 'admin', '100.00', '2000.0', 'dragon,dragon,dragon', '2023-06-15 17:50:08'),
('SM-012', 'admin', '100.00', '2000.0', 'dragon,dragon,dragon', '2023-06-15 17:50:17'),
('SM-013', 'admin', '100.00', '2000.0', 'dragon,dragon,dragon', '2023-06-15 17:50:52'),
('SM-014', 'admin', '100.00', '2000.0', 'dragon,dragon,dragon', '2023-06-15 17:50:57'),
('SM-015', 'admin', '100.00', '2000.0', 'dragon,dragon,dragon', '2023-06-15 17:51:07'),
('SM-016', 'admin', '100.00', '2000.0', 'dragon,dragon,dragon', '2023-06-15 17:52:42'),
('SM-017', 'admin', '100.00', '2000.0', 'dragon,dragon,dragon', '2023-06-15 18:34:59'),
('SM-018', 'admin', '100.00', '2000.0', 'dragon,dragon,dragon', '2023-06-15 18:41:15'),
('SM-019', 'admin', '100.00', '2000.0', 'dragon,dragon,dragon', '2023-06-15 18:41:28'),
('SM-020', 'admin', '100.00', '2000.0', 'dragon,dragon,dragon', '2023-06-15 18:42:14'),
('SM-021', 'admin', '1.00', '20.0', 'dragon,dragon,dragon', '2023-10-16 17:03:55'),
('SM-022', 'admin', '1.00', '20.0', 'dragon,dragon,dragon', '2023-10-16 17:41:51'),
('SM-023', 'admin', '10.00', '200.0', 'dragon,dragon,dragon', '2023-10-16 17:44:19'),
('SM-024', 'admin', '10.00', '200.0', 'dragon,dragon,dragon', '2023-10-16 17:46:01'),
('SM-025', 'admin', '10.00', '200.0', 'dragon,dragon,dragon', '2023-10-16 17:48:55'),
('SM-026', 'admin', '10.00', '200.0', 'dragon,dragon,dragon', '2023-10-16 19:43:24'),
('SM-027', 'admin', '10.00', '200.0', 'dragon,dragon,dragon', '2023-10-16 19:43:57'),
('SM-028', 'admin', '10.00', '200.0', 'dragon,dragon,dragon', '2023-10-16 19:44:02'),
('SM-029', 'admin', '10.00', '200.0', 'dragon,dragon,dragon', '2023-10-16 19:44:04'),
('SM-030', 'admin', '10.00', '200.0', 'dragon,dragon,dragon', '2023-10-16 19:44:08');

--
-- Triggers `slot_machine_history`
--
DELIMITER $$
CREATE TRIGGER `slotmachineid_tri` BEFORE INSERT ON `slot_machine_history` FOR EACH ROW BEGIN
    DECLARE next_id VARCHAR(10);
    SELECT CONCAT('SM-', LPAD((SUBSTRING(MAX(sm_id), 4) + 1), 3, '0')) INTO next_id FROM slot_machine_history;
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
-- Table structure for table `transaction`
--

CREATE TABLE `transaction` (
  `transaction_id` varchar(96) NOT NULL,
  `transaction_id2` varchar(96) NOT NULL,
  `user` varchar(96) NOT NULL,
  `amt_bef_transaction` decimal(9,2) NOT NULL,
  `amt_aft_transaction` decimal(9,2) NOT NULL,
  `total_amt_transaction` decimal(9,2) NOT NULL,
  `transaction_time` datetime NOT NULL DEFAULT current_timestamp(),
  `transaction_comment` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Triggers `transaction`
--
DELIMITER $$
CREATE TRIGGER `transaction_id` BEFORE INSERT ON `transaction` FOR EACH ROW BEGIN
    DECLARE next_id INT;
    SELECT (SUBSTRING(MAX(transaction_id), 6) + 1) INTO next_id FROM transaction;
    
    IF next_id IS NULL THEN
        SET next_id = 1;
    END IF;

    WHILE (SELECT COUNT(*) FROM transaction WHERE transaction_id = CONCAT('TRANS-', LPAD(next_id, 5, '0'))) > 0 DO
        SET next_id = next_id + 1;
    END WHILE;
    
    SET NEW.transaction_id = CONCAT('TRANS-', LPAD(next_id, 5, '0'));
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
  `priv` varchar(20) NOT NULL DEFAULT 'user',
  `balance` decimal(12,2) NOT NULL DEFAULT 0.00,
  `last_login` datetime DEFAULT NULL,
  `last_logout` datetime DEFAULT NULL,
  `status` varchar(10) NOT NULL DEFAULT 'active'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`username`, `password`, `priv`, `balance`, `last_login`, `last_logout`, `status`) VALUES
('admin', 'admin', 'admin', '55.00', '2023-10-20 12:29:07', '2023-10-20 12:27:16', 'active'),
('banker', 'banker', 'banker', '83950831.99', NULL, '2023-10-19 16:57:52', 'active'),
('user1', 'user1', 'user', '1000.00', '2023-10-16 17:38:38', '2023-10-16 17:38:39', 'active'),
('user2', 'user2', 'user', '100.00', NULL, NULL, 'active');

--
-- Triggers `user`
--
DELIMITER $$
CREATE TRIGGER `status_tri` AFTER INSERT ON `user` FOR EACH ROW BEGIN
    UPDATE user
    SET status = 'active'
    WHERE username = NEW.username;
END
$$
DELIMITER ;

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
('WL-001', 'admin', 1000, 'win', '2023-06-15 17:39:47'),
('WL-002', 'admin', 100, 'win', '2023-06-15 18:34:54'),
('WL-003', 'admin', 1, 'loss', '2023-10-20 12:05:57'),
('WL-004', 'admin', 21, 'win', '2023-10-20 12:07:57'),
('WL-005', 'admin', 99, 'loss', '2023-10-20 12:12:15'),
('WL-006', 'admin', 11012, 'loss', '2023-10-20 12:12:44');

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
-- Indexes for table `slot_machine_history`
--
ALTER TABLE `slot_machine_history`
  ADD PRIMARY KEY (`sm_id`);

--
-- Indexes for table `topup_history`
--
ALTER TABLE `topup_history`
  ADD PRIMARY KEY (`topup_id`);

--
-- Indexes for table `transaction`
--
ALTER TABLE `transaction`
  ADD PRIMARY KEY (`transaction_id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`username`);

--
-- Indexes for table `winloss_history`
--
ALTER TABLE `winloss_history`
  ADD PRIMARY KEY (`winloss_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
