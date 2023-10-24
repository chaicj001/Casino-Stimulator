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
-- Database: `casino_regis`
--

-- --------------------------------------------------------

--
-- Table structure for table `referal`
--

CREATE TABLE `referal` (
  `referal_code` varchar(96) NOT NULL,
  `balance` decimal(9,2) NOT NULL,
  `user_priv` varchar(10) NOT NULL,
  `created_by` varchar(96) NOT NULL,
  `created_time` varchar(96) NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `referal`
--

INSERT INTO `referal` (`referal_code`, `balance`, `user_priv`, `created_by`, `created_time`) VALUES
('07bSzKXkGY', '3202.00', 'user', 'admin', '2023-06-24 18:22:58'),
('1W5NbllvsI', '8558.00', 'user', 'admin', '2023-06-19 17:05:00'),
('1zayXe1zg7', '17494.00', 'user', 'admin', '2023-06-19 17:05:01'),
('2MJC2MqIQb', '13637.00', 'user', 'banker', '2023-06-19 17:05:42'),
('33UP5D6ruh', '100000.00', 'user', 'banker', '2023-06-19 17:05:38'),
('34XI7Bb5KV', '3757.00', 'user', 'admin', '2023-06-24 18:37:35'),
('3BbETRqqTZ', '7407.00', 'user', 'admin', '2023-06-19 17:05:00'),
('3tpDTEw2qt', '100000.00', 'user', 'banker', '2023-06-19 17:05:38'),
('44YZVzQdEC', '4404.00', 'user', 'admin', '2023-06-24 18:37:24'),
('4nQhAKRDTX', '3970.00', 'user', 'admin', '2023-06-24 18:22:58'),
('4rWfCjNnAH', '50000.00', 'user', 'admin', '2023-06-19 17:05:03'),
('69536RvxDR', '3425.00', 'user', 'admin', '2023-06-19 17:04:58'),
('6FXWJ3kabd', '100000.00', 'user', 'admin', '2023-06-19 17:05:04'),
('6NFNeze1dp', '100000.00', 'user', 'banker', '2023-06-19 17:05:38'),
('7l778Ppi8Z', '50000.00', 'user', 'banker', '2023-06-19 17:05:40'),
('9HofQkHCdK', '50000.00', 'user', 'banker', '2023-06-19 17:05:40'),
('9wa5qMh5DY', '4190.00', 'user', 'admin', '2023-06-24 18:37:24'),
('aaFv37WwOA', '15947.00', 'user', 'banker', '2023-06-19 17:05:42'),
('AbGpldDorK', '50000.00', 'user', 'admin', '2023-06-19 17:05:03'),
('aOXBmNdPvx', '4562.00', 'user', 'admin', '2023-06-24 18:22:58'),
('Asr2cTFRYz', '1000000.00', 'banker', 'banker', '2023-06-19 17:05:33'),
('b4z78DcTOi', '50000.00', 'user', 'admin', '2023-06-19 17:05:03'),
('BawSJ7i0b7', '100000.00', 'user', 'banker', '2023-06-19 17:05:38'),
('bE5bmXK0Xq', '3506.00', 'user', 'banker', '2023-06-19 17:05:45'),
('bfNPJvuNqT', '3665.00', 'user', 'admin', '2023-06-24 18:37:24'),
('BMEO6tKZ91', '16184.00', 'user', 'banker', '2023-06-19 17:05:42'),
('Bnke2tOgB8', '3913.00', 'user', 'admin', '2023-06-24 18:37:35'),
('bO0VmkBAP4', '50000.00', 'user', 'banker', '2023-06-19 17:05:40'),
('c1zrCebYT1', '7992.00', 'user', 'banker', '2023-06-19 17:05:44'),
('c9dNhjVcvH', '1000000.00', 'banker', 'admin', '2023-06-19 17:05:06'),
('CUdOonaVOY', '11045.00', 'user', 'banker', '2023-06-19 17:05:42'),
('cw5nTXFo5Y', '2441.00', 'user', 'admin', '2023-06-24 18:37:35'),
('d6MpfhDggC', '5322.00', 'user', 'banker', '2023-06-19 17:05:44'),
('drDznPqFZ7', '3988.00', 'user', 'admin', '2023-06-19 17:04:58'),
('Du59Q2cpmt', '100000.00', 'user', 'banker', '2023-06-19 17:05:38'),
('DV6lLFqT8w', '3367.00', 'user', 'admin', '2023-06-19 17:04:58'),
('Ebpu52jYLA', '17920.00', 'user', 'admin', '2023-06-19 17:05:01'),
('ExrMeQgA4W', '5358.00', 'user', 'admin', '2023-06-19 17:05:00'),
('fds6f3oPjj', '3589.00', 'user', 'admin', '2023-06-24 18:37:24'),
('fhdh3oiNgs', '8517.00', 'user', 'banker', '2023-06-19 17:05:44'),
('FIh9ytPmHv', '2153.00', 'user', 'admin', '2023-06-24 18:37:24'),
('fJ5wyeeEZe', '2762.00', 'user', 'admin', '2023-06-24 18:22:58'),
('fJHamhSa0r', '3651.00', 'user', 'admin', '2023-06-24 18:22:58'),
('fMhkkJoQNU', '50000.00', 'user', 'admin', '2023-06-19 17:05:03'),
('FpQkZKkRAi', '3918.00', 'user', 'banker', '2023-06-19 17:05:45'),
('g9uewVUk5k', '3803.00', 'user', 'admin', '2023-06-19 17:04:58'),
('GcOJtWUSJn', '50000.00', 'user', 'banker', '2023-06-19 17:05:40'),
('GE00NHuoWs', '20363.00', 'user', 'admin', '2023-06-19 17:05:01'),
('gfiyfsSNRI', '14352.00', 'user', 'banker', '2023-06-19 17:05:42'),
('gRzXB1Ypa2', '1000000.00', 'banker', 'banker', '2023-06-19 17:05:33'),
('GXBNMwZxcp', '2302.00', 'user', 'banker', '2023-06-19 17:05:45'),
('h30q82OTuK', '50000.00', 'user', 'banker', '2023-06-19 17:05:40'),
('HGyOrmYsOw', '50000.00', 'user', 'banker', '2023-06-19 17:05:40'),
('i3l7a4ZTO9', '8584.00', 'user', 'admin', '2023-06-19 17:05:00'),
('inKTRM2efJ', '6670.00', 'user', 'banker', '2023-06-19 17:05:44'),
('iokzdnPNv0', '11244.00', 'user', 'banker', '2023-06-19 17:05:42'),
('IQ2CPcHB8J', '4111.00', 'user', 'admin', '2023-06-24 18:22:58'),
('ISqNLlS56Z', '100000.00', 'user', 'admin', '2023-06-19 17:05:04'),
('IyHAJW5Q54', '8306.00', 'user', 'banker', '2023-06-19 17:05:44'),
('IYZibz20FB', '8619.00', 'user', 'admin', '2023-06-19 17:05:00'),
('jcYfWuDITB', '7059.00', 'user', 'admin', '2023-06-19 17:05:00'),
('JfoLQWYgsC', '3135.00', 'user', 'banker', '2023-06-19 17:05:45'),
('jG9UiSu5tc', '6270.00', 'user', 'banker', '2023-06-19 17:05:44'),
('JIMSOWNZvK', '1000000.00', 'banker', 'banker', '2023-06-19 17:05:34'),
('jztSIoV0R3', '4573.00', 'user', 'banker', '2023-06-19 17:05:45'),
('K2JXpsMH8E', '1000000.00', 'banker', 'admin', '2023-06-19 17:05:06'),
('k2RmB39cee', '1000000.00', 'banker', 'admin', '2023-06-19 17:05:06'),
('KJKTPMlzOg', '100000.00', 'user', 'banker', '2023-06-19 17:05:38'),
('KnWIioI09z', '100000.00', 'user', 'admin', '2023-06-19 17:05:04'),
('KW6zhYs1WR', '4072.00', 'user', 'admin', '2023-06-24 18:22:58'),
('KwDzTPnQPE', '3112.00', 'user', 'banker', '2023-06-19 17:05:45'),
('lMkTm7IhZX', '9317.00', 'user', 'admin', '2023-06-19 17:05:00'),
('lSyDbuhSzo', '2265.00', 'user', 'admin', '2023-06-24 18:22:58'),
('LTXXYLJDZt', '100000.00', 'user', 'banker', '2023-06-19 17:05:38'),
('LUgql4XocG', '100000.00', 'user', 'admin', '2023-06-19 17:05:04'),
('LyYf8E7FOW', '3377.00', 'user', 'banker', '2023-06-19 17:05:45'),
('maZIdXYTIp', '3522.00', 'user', 'admin', '2023-06-24 18:37:35'),
('mFae3U057k', '50000.00', 'user', 'banker', '2023-06-19 17:05:40'),
('MmjFfvrYx1', '4464.00', 'user', 'admin', '2023-06-24 18:37:24'),
('MMvrdA1vaA', '1000000.00', 'banker', 'banker', '2023-06-19 17:05:33'),
('moOXOsfbOT', '2742.00', 'user', 'admin', '2023-06-19 17:04:58'),
('MOw4LKasDL', '100000.00', 'user', 'admin', '2023-06-19 17:05:04'),
('MQvKMgoTsT', '4349.00', 'user', 'admin', '2023-06-24 18:22:58'),
('NfQfZNHtvv', '4957.00', 'user', 'admin', '2023-06-19 17:04:58'),
('nzBYsGv2Av', '50000.00', 'user', 'admin', '2023-06-19 17:05:03'),
('O79ZEB29lM', '3405.00', 'user', 'admin', '2023-06-19 17:04:58'),
('oAaNfGYL9a', '100000.00', 'user', 'banker', '2023-06-19 17:05:38'),
('OdmaZYrH9o', '2499.00', 'user', 'banker', '2023-06-19 17:05:45'),
('oXX3Ti9JnA', '2406.00', 'user', 'admin', '2023-06-24 18:37:35'),
('PHnqvWQY6W', '3853.00', 'user', 'admin', '2023-06-24 18:37:24'),
('podHU8Tt72', '3140.00', 'user', 'admin', '2023-06-24 18:37:35'),
('PQt798yn5A', '24101.00', 'user', 'banker', '2023-06-19 17:05:42'),
('PtG2fiSFYr', '1000000.00', 'banker', 'banker', '2023-06-19 17:05:34'),
('q0fdiZaRRE', '100000.00', 'user', 'admin', '2023-06-19 17:05:04'),
('q26KBZll0s', '2822.00', 'user', 'banker', '2023-06-19 17:05:45'),
('QfhhL8cu59', '19848.00', 'user', 'banker', '2023-06-19 17:05:42'),
('QGTNYF5VeE', '50000.00', 'user', 'banker', '2023-06-19 17:05:40'),
('QQJyxdtj4k', '1000000.00', 'banker', 'banker', '2023-06-19 17:05:34'),
('qslZq4xzeM', '100000.00', 'user', 'admin', '2023-06-19 17:05:04'),
('qtTgagwxR1', '8360.00', 'user', 'admin', '2023-06-19 17:05:00'),
('Qxqpuuri4p', '50000.00', 'user', 'admin', '2023-06-19 17:05:03'),
('RfG0u5gK1L', '4053.00', 'user', 'banker', '2023-06-19 17:05:45'),
('RLA5tVwN5a', '50000.00', 'user', 'admin', '2023-06-19 17:05:03'),
('RYC0OT8974', '1000000.00', 'banker', 'banker', '2023-06-19 17:05:33'),
('S0T2Cj3am4', '4194.00', 'user', 'admin', '2023-06-24 18:37:35'),
('Svq4Gr1dWZ', '9187.00', 'user', 'banker', '2023-06-19 17:05:44'),
('Tb8Kmims6K', '12645.00', 'user', 'admin', '2023-06-19 17:05:01'),
('tC2KeF9ce1', '100000.00', 'user', 'banker', '2023-06-19 17:05:38'),
('tHD8sZSNoP', '24237.00', 'user', 'banker', '2023-06-19 17:05:42'),
('TOtOClgpDn', '3920.00', 'user', 'admin', '2023-06-24 18:37:24'),
('tRsllFSTWk', '50000.00', 'user', 'banker', '2023-06-19 17:05:40'),
('u5dYa3dLlX', '12143.00', 'user', 'admin', '2023-06-19 17:05:01'),
('uhtcADau4L', '1000000.00', 'banker', 'banker', '2023-06-19 17:05:33'),
('UlgUViewaM', '100000.00', 'user', 'admin', '2023-06-19 17:05:04'),
('uVP71yaqC3', '1000000.00', 'banker', 'admin', '2023-06-19 17:05:06'),
('vgviJYzvYe', '14787.00', 'user', 'admin', '2023-06-19 17:05:01'),
('VSLJMXNGBg', '6540.00', 'user', 'banker', '2023-06-19 17:05:44'),
('w6wqpinokn', '21291.00', 'user', 'banker', '2023-06-19 17:05:42'),
('WBSQ4oNtrX', '23788.00', 'user', 'admin', '2023-06-19 17:05:01'),
('WjfcMOvuyx', '24053.00', 'user', 'admin', '2023-06-19 17:05:01'),
('WjV1YQIgIR', '4134.00', 'user', 'admin', '2023-06-19 17:04:58'),
('Wo73bQLddg', '4968.00', 'user', 'admin', '2023-06-19 17:04:58'),
('wPfZ9qlIJ1', '50000.00', 'user', 'admin', '2023-06-19 17:05:03'),
('wulYZWUp7e', '4012.00', 'user', 'admin', '2023-06-24 18:37:24'),
('wx42aBZVog', '2822.00', 'user', 'admin', '2023-06-24 18:37:35'),
('xGiNQFjm77', '23312.00', 'user', 'admin', '2023-06-19 17:05:01'),
('XLX5nEdaNF', '50000.00', 'user', 'admin', '2023-06-19 17:05:03'),
('XSMt93kdXa', '4919.00', 'user', 'admin', '2023-06-24 18:37:35'),
('Ya7vGMaO4c', '5454.00', 'user', 'banker', '2023-06-19 17:05:44'),
('yHU47DevSv', '3250.00', 'user', 'admin', '2023-06-24 18:22:58'),
('yof20s79wl', '2210.00', 'user', 'admin', '2023-06-24 18:37:24'),
('yP66ZlkZDW', '6925.00', 'user', 'admin', '2023-06-19 17:05:00'),
('YVWeHCb91c', '2294.00', 'user', 'admin', '2023-06-19 17:04:58'),
('zE32JOOHvc', '50000.00', 'user', 'banker', '2023-06-19 17:05:40'),
('zi2LcJiCso', '50000.00', 'user', 'admin', '2023-06-19 17:05:03'),
('ZMDNDYVLLt', '11601.00', 'user', 'admin', '2023-06-19 17:05:01');

-- --------------------------------------------------------

--
-- Table structure for table `referal_tran`
--

CREATE TABLE `referal_tran` (
  `reftransaction_id` varchar(96) NOT NULL,
  `referal_code` varchar(96) NOT NULL,
  `balance` double(9,2) NOT NULL,
  `trans_time` varchar(96) NOT NULL DEFAULT current_timestamp(),
  `user_from` varchar(96) NOT NULL,
  `user_to` varchar(96) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `referal_tran`
--

INSERT INTO `referal_tran` (`reftransaction_id`, `referal_code`, `balance`, `trans_time`, `user_from`, `user_to`) VALUES
('', '0XPpmjlkv8', 18163.00, '2023-06-16 18:11:06', '', 'admin'),
('', '1TIuzmzsh7', 3300.00, '2023-06-16 18:14:15', '', 'admin'),
('', '4bxLuFE423', 100000.00, '2023-06-16 18:15:43', '', 'admin'),
('', 'zHmxRd4myO', 1000000.00, '2023-06-19 17:06:09', 'banker', 'admin'),
('', '2H9TUmRIoG', 100000.00, '2023-06-19 17:07:13', 'admin', 'admin'),
('', '1tlm1eUC3x', 7799.00, '2023-06-19 17:10:11', 'admin', 'admin'),
('', '0P92DRjt69', 6975.00, '2023-06-19 17:10:35', 'banker', 'admin'),
('REFTRANS-00001', '0VdNP4O8af', 100000.00, '2023-06-24 18:11:28', 'admin', 'admin'),
('REFTRANS-00002', 'y0L4xZFwmh', 1000000.00, '2023-06-24 18:11:49', 'banker', 'admin'),
('REFTRANS-00003', 'AdpOXT8N5H', 1000000.00, '2023-10-02 21:29:02', 'admin', 'admin'),
('REFTRANS-00004', '0x5kaijcT2', 100000.00, '2023-10-02 21:29:43', 'banker', 'admin'),
('REFTRANS-00005', '2cBjrMpqnK', 3645.00, '2023-10-02 21:32:15', 'admin', 'admin');

--
-- Triggers `referal_tran`
--
DELIMITER $$
CREATE TRIGGER `reftran_id` BEFORE INSERT ON `referal_tran` FOR EACH ROW BEGIN
    DECLARE next_id INT;
    SELECT (SUBSTRING(MAX(reftransaction_id), 6) + 1) INTO next_id FROM referal_tran;
    
    IF next_id IS NULL THEN
        SET next_id = 1;
    END IF;

    WHILE (SELECT COUNT(*) FROM referal_tran WHERE reftransaction_id = CONCAT('REFTRANS-', LPAD(next_id, 5, '0'))) > 0 DO
        SET next_id = next_id + 1;
    END WHILE;
    
    SET NEW.reftransaction_id = CONCAT('REFTRANS-', LPAD(next_id, 5, '0'));
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `register`
--

CREATE TABLE `register` (
  `username` varchar(96) NOT NULL,
  `password` varchar(96) NOT NULL,
  `referal` varchar(10) NOT NULL,
  `submit_time` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `referal`
--
ALTER TABLE `referal`
  ADD PRIMARY KEY (`referal_code`);

--
-- Indexes for table `register`
--
ALTER TABLE `register`
  ADD PRIMARY KEY (`username`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
