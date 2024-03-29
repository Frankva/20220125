
CREATE TABLE `user_sync` (
  `id_user` int(11) NOT NULL AUTO_INCREMENT,
  `name` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `surname` text COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id_user`)
) ENGINE=InnoDB AUTO_INCREMENT=107 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `user_type` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(45) COLLATE utf8mb4_unicode_ci NOT NULL,
  `access_level` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ;

CREATE TABLE `ci_user` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `fk_user_type` int(10) unsigned NOT NULL,
  `username` varchar(45) COLLATE utf8mb4_unicode_ci NOT NULL,
  `password` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `archive` timestamp NULL DEFAULT NULL,
  `date_creation` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  FOREIGN KEY(`fk_user_type`) REFERENCES `user_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ;

CREATE TABLE `access_tim_user` (
  `id_access` int(11) NOT NULL AUTO_INCREMENT,
  `id_user` int(11) NOT NULL,
  `id_ci_user` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id_access`),
  FOREIGN KEY (`id_user`) REFERENCES `user_sync` (`id_user`),
  FOREIGN KEY (`id_ci_user`) REFERENCES `ci_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=53 DEFAULT CHARSET=utf8mb4 ;

CREATE TABLE `badge_sync` (
  `id_badge` bigint(20) NOT NULL,
  `id_user` int(11) NOT NULL,
  PRIMARY KEY (`id_badge`),
  FOREIGN KEY (`id_user`) REFERENCES `user_sync` (`id_user`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `badge_write` (
  `id_badge` bigint(20) NOT NULL,
  `id_user` int(11) NOT NULL,
  PRIMARY KEY (`id_badge`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ;

CREATE TABLE `ci_sessions` (
  `id` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `ip_address` varchar(45) COLLATE utf8mb4_unicode_ci NOT NULL,
  `timestamp` int(10) unsigned NOT NULL,
  `data` blob NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ;

CREATE TABLE `fake_log` (
  `id_fake_log` int(11) NOT NULL AUTO_INCREMENT,
  `id_user` int(11) NOT NULL,
  `id_ci_user` int(10) unsigned NOT NULL,
  `date` datetime NOT NULL,
  `date_site` datetime NOT NULL DEFAULT current_timestamp(),
  `inside` tinyint(1) NOT NULL,
  PRIMARY KEY (`id_fake_log`),
  FOREIGN KEY (`id_user`) REFERENCES `user_sync` (`id_user`),
  FOREIGN KEY (`id_ci_user`) REFERENCES `ci_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ;

CREATE TABLE `log_sync` (
  `date` datetime NOT NULL,
  `id_badge` bigint(20) NOT NULL,
  `inside` tinyint(1) DEFAULT NULL,
  `id_log` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id_log`),
  FOREIGN KEY (`id_badge`) REFERENCES `badge_sync` (`id_badge`)
) ENGINE=InnoDB AUTO_INCREMENT=238 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `log_write` (
  `date` datetime NOT NULL DEFAULT current_timestamp(),
  `id_badge` bigint(20) NOT NULL,
  `inside` tinyint(1) NOT NULL,
  `id_log` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id_log`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ;

CREATE TABLE `user_write` (
  `id_user` int(11) NOT NULL AUTO_INCREMENT,
  `name` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `surname` text COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id_user`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ;



CREATE VIEW `log` AS 
SELECT * FROM `log_sync`
UNION
SELECT * FROM `log_write`
WHERE (`date`, `id_badge`, `inside`) NOT IN (SELECT `date`, `id_badge`, `inside` FROM `log_sync`)
ORDER BY `date`;

CREATE VIEW `user` AS 
SELECT * FROM `user_sync`
UNION
SELECT * FROM `user_write`
WHERE (`name`, `surname`) NOT IN (SELECT `name`, `surname` FROM `user_sync`)
ORDER BY `name`;

CREATE VIEW `badge` AS 
SELECT * FROM `badge_sync`
UNION
SELECT * FROM `badge_write`
WHERE (`id_badge`, `id_user`) NOT IN (SELECT `id_badge`, `id_user` FROM `badge_sync`);


CREATE VIEW log_fake_log AS 
SELECT `date`, `id_user`, `inside`, `id_fake_log` FROM `fake_log`
UNION
SELECT `date`, `id_user`, `inside`, NULL FROM `log`, `badge` WHERE `badge`.`id_badge` = `log`.`id_badge` 
ORDER BY `date`;



LOCK TABLES `user_sync` WRITE;
INSERT INTO `user_sync` VALUES
(92,'Marc','PORTA'),
(93,'David','AESCHLIMANN'),
(94,'Dylan','DERVEY'),
(95,'Aleksa','BLAGOJEVIC'),
(96,'Elia','FORTUNATO'),
(97,'Caroline','ARM'),
(98,'David','Silvestre'),
(106,'Prénom','test');
UNLOCK TABLES;

LOCK TABLES `user_type` WRITE;
INSERT INTO `user_type` VALUES
(1,'Administrateur',4),
(2,'Enregistré',2),
(3,'Invité',1);
UNLOCK TABLES;

LOCK TABLES `ci_user` WRITE;
INSERT INTO `ci_user` VALUES
(6,1,'admin','$2y$10$84r63xo.M4LVcIi8IvT8cO0qYxyglPshY1jJmKLedRMcaTcxhcVYO',NULL,NULL,'2022-06-13 11:40:08'),
(7,2,'utilisateur','$2y$10$xgNNdbyyon6zsHEJjiDC6eujenELwnW67emQuK3DwEpKJgXaqvmSy',NULL,NULL,'2022-06-13 11:40:08'),
(8,2,'PoMa','$2y$10$.toUqNqTV5Opwx/Jrgi5vu7MU6Gz.h/zm91cIPCiIIPcdOKzKcz56','MarcLouis.Porta@formation.orif.ch',NULL,'2022-07-01 12:21:55'),
(9,2,'BlAl','$2y$10$XJkh4vgVZgib0Y0FLb8.MO7ekgYgmZdbZaf7RLLabFRI/YWlAiSSi','Aleksa.BlagojevicMartins@formation.orif.ch',NULL,'2022-07-06 11:48:50'),
(10,2,'AeDa','$2y$10$OT5aJdn6GNyb5H86Eqa3suoEJg6FgW6I0UNIIg7F3DAlYikzu4eGq','David.Aeschlimann@formation.orif.ch',NULL,'2022-07-11 12:15:57'),
(11,2,'DeDy','$2y$10$jf660rMCIk9Jv0qYYhpNKevnYcA4sppJKSE8/AM/uMo5QqEALc2U6','DylanQuentin.Dervey@formation.orif.ch',NULL,'2022-07-11 12:19:04'),
(12,2,'FoEl','$2y$10$20pdsipqEF93WCywxKaISexTCMMYCSH/sVIkTTlPilei4w3nleK/.','Elia.Fortunato@formation.orif.ch',NULL,'2022-07-11 12:22:57'),
(13,2,'ArCa','$2y$10$cn/bp/av.4ENZOYYSC4KIO8bkKg7gBpjwyXN//p.Gfn4512KCOf2e','CarolineLouiseAnne.Arm@formation.orif.ch',NULL,'2022-07-11 12:25:11'),
(14,2,'TeDa','$2y$10$QO36PRRmIokSK1DRs7kC3.h.bESyd34seqzWF0dFXqnxrUdq/9GwK','David.Silvestre@orif.ch',NULL,'2022-07-11 12:31:57');
UNLOCK TABLES;

LOCK TABLES `access_tim_user` WRITE;
INSERT INTO `access_tim_user` VALUES
(4,95,9),
(42,94,11),
(43,96,12),
(44,97,13),
(45,98,14),
(50,92,8);
UNLOCK TABLES;

LOCK TABLES `badge_sync` WRITE;
INSERT INTO `badge_sync` VALUES
(589402514225,92),
(483985410385,93),
(726118152451,94),
(45336916925,95),
(720037247467,96),
(904305210343,97),
(156025193255,98),
(42,106);
UNLOCK TABLES;

LOCK TABLES `log_sync` WRITE;
INSERT INTO `log_sync` VALUES
('2022-05-17 15:36:16',589402514225,1,1),
('2022-05-17 15:36:41',589402514225,0,2),
('2022-05-17 15:37:00',589402514225,1,3),
('2022-05-17 16:45:16',589402514225,0,4),
('2022-05-18 07:58:27',589402514225,1,5),
('2022-05-18 07:59:02',45336916925,1,6),
('2022-05-18 08:01:44',483985410385,1,7),
('2022-05-18 09:08:19',904305210343,1,8),
('2022-05-18 10:07:12',720037247467,1,9),
('2022-05-18 12:00:04',45336916925,0,10),
('2022-05-18 12:00:10',720037247467,0,11),
('2022-05-18 12:00:20',483985410385,0,12),
('2022-05-18 12:00:28',589402514225,0,13),
('2022-05-18 12:00:38',904305210343,0,14),
('2022-05-18 12:31:27',589402514225,1,15),
('2022-05-18 12:33:37',589402514225,1,16),
('2022-05-18 12:46:38',45336916925,1,17),
('2022-05-18 12:47:06',720037247467,1,18),
('2022-05-18 12:47:34',483985410385,1,19),
('2022-05-18 12:47:45',904305210343,1,20),
('2022-05-18 15:56:50',720037247467,0,21),
('2022-05-18 15:59:02',483985410385,0,22),
('2022-05-18 16:47:29',589402514225,0,23),
('2022-05-18 16:47:40',904305210343,0,24),
('2022-05-18 16:48:31',45336916925,0,25),
('2022-05-19 07:52:42',589402514225,1,26),
('2022-05-19 07:56:15',483985410385,1,27),
('2022-05-19 07:58:40',45336916925,1,28),
('2022-05-19 09:29:30',904305210343,1,29),
('2022-05-19 10:03:32',720037247467,1,30),
('2022-05-19 11:59:45',45336916925,0,31),
('2022-05-19 11:59:59',483985410385,0,32),
('2022-05-19 12:00:06',904305210343,0,33),
('2022-05-19 12:00:56',589402514225,0,34),
('2022-05-19 12:38:09',589402514225,1,35),
('2022-05-19 12:46:47',483985410385,1,36),
('2022-05-19 12:46:54',904305210343,1,37),
('2022-05-19 12:48:04',726118152451,1,38),
('2022-05-19 12:48:28',720037247467,1,39),
('2022-05-19 12:48:32',45336916925,1,40),
('2022-05-19 16:03:40',483985410385,0,41),
('2022-05-19 16:49:08',45336916925,0,42),
('2022-05-19 16:49:20',726118152451,0,43),
('2022-05-19 16:50:08',589402514225,0,44),
('2022-05-20 07:53:57',589402514225,1,45),
('2022-05-20 07:54:35',483985410385,1,46),
('2022-05-20 08:03:01',45336916925,1,47),
('2022-05-20 08:05:17',726118152451,1,48),
('2022-05-20 08:09:22',904305210343,1,49),
('2022-05-20 12:00:44',589402514225,0,50),
('2022-05-20 12:00:48',45336916925,0,51),
('2022-05-20 12:00:51',483985410385,0,52),
('2022-05-20 12:00:56',904305210343,0,53),
('2022-05-20 12:39:06',589402514225,1,54),
('2022-05-20 13:28:26',904305210343,1,55),
('2022-05-20 13:28:28',904305210343,0,56),
('2022-05-20 14:36:05',483985410385,0,57),
('2022-05-20 16:48:42',589402514225,0,58),
('2022-05-20 16:56:52',45336916925,0,59),
('2022-05-23 09:00:15',904305210343,1,60),
('2022-05-23 09:00:47',45336916925,1,61),
('2022-05-23 12:00:33',45336916925,0,62),
('2022-05-23 12:00:37',904305210343,0,63),
('2022-05-23 12:30:58',720037247467,1,64),
('2022-05-23 12:37:58',589402514225,1,65),
('2022-05-23 12:48:54',904305210343,1,66),
('2022-05-23 12:49:25',45336916925,1,67),
('2022-05-23 15:46:48',720037247467,0,68),
('2022-05-23 16:45:58',904305210343,0,69),
('2022-05-23 16:48:39',45336916925,0,70),
('2022-05-24 07:53:20',589402514225,1,71),
('2022-05-24 07:58:26',45336916925,1,72),
('2022-05-24 09:31:37',904305210343,1,73),
('2022-05-24 12:00:46',589402514225,0,74),
('2022-05-24 12:00:54',45336916925,0,75),
('2022-05-24 12:29:59',720037247467,1,76),
('2022-05-24 12:39:40',589402514225,1,77),
('2022-05-24 12:43:04',904305210343,0,78),
('2022-05-24 12:43:06',904305210343,1,79),
('2022-05-24 12:43:14',45336916925,1,80),
('2022-05-24 16:46:39',904305210343,0,81),
('2022-05-24 16:48:06',45336916925,0,82),
('2022-05-24 16:50:29',589402514225,0,83),
('2022-05-25 07:55:48',589402514225,1,84),
('2022-05-25 07:59:34',904305210343,1,85),
('2022-05-25 08:00:13',45336916925,1,86),
('2022-05-25 08:01:19',483985410385,1,87),
('2022-05-25 10:06:50',720037247467,1,88),
('2022-05-25 12:00:18',589402514225,0,89),
('2022-05-25 12:00:24',904305210343,0,90),
('2022-05-25 12:00:27',483985410385,0,91),
('2022-05-25 12:00:37',45336916925,0,92),
('2022-05-25 12:32:15',589402514225,1,93),
('2022-05-25 12:47:47',45336916925,1,94),
('2022-05-25 12:58:24',904305210343,1,95),
('2022-05-25 12:58:29',904305210343,1,96),
('2022-05-25 12:58:44',483985410385,1,97),
('2022-05-25 15:44:56',720037247467,0,98),
('2022-05-25 15:46:09',904305210343,0,99),
('2022-05-25 15:46:13',483985410385,0,100),
('2022-05-25 15:47:30',589402514225,0,101),
('2022-05-25 15:47:35',45336916925,0,102),
('2022-05-30 09:02:10',904305210343,1,103),
('2022-05-30 10:00:10',720037247467,1,104),
('2022-05-30 10:33:06',45336916925,1,105),
('2022-05-30 12:00:03',45336916925,0,106),
('2022-05-30 12:00:15',904305210343,0,107),
('2022-05-30 12:01:08',720037247467,0,108),
('2022-05-30 12:41:45',589402514225,1,109),
('2022-05-30 12:46:34',720037247467,1,110),
('2022-05-30 12:46:45',45336916925,1,111),
('2022-05-30 12:46:54',904305210343,1,112),
('2022-05-30 15:47:27',720037247467,0,113),
('2022-05-30 16:47:17',904305210343,0,114),
('2022-05-30 16:47:51',45336916925,0,115),
('2022-05-31 07:52:03',589402514225,1,116),
('2022-05-31 08:01:21',45336916925,1,117),
('2022-05-31 10:05:55',720037247467,1,118),
('2022-05-31 12:00:16',720037247467,0,119),
('2022-05-31 12:00:29',589402514225,0,120),
('2022-05-31 12:00:33',45336916925,0,121),
('2022-05-31 12:36:51',589402514225,1,122),
('2022-05-31 12:46:47',720037247467,1,123),
('2022-05-31 12:46:50',45336916925,1,124),
('2022-05-31 12:48:48',156025193255,1,125),
('2022-05-31 16:45:25',156025193255,0,126),
('2022-05-31 16:45:36',45336916925,0,127),
('2022-05-31 16:45:41',589402514225,0,128),
('2022-06-01 07:57:35',589402514225,1,129),
('2022-06-01 07:57:54',45336916925,1,130),
('2022-06-01 08:00:29',156025193255,1,131),
('2022-06-01 10:01:42',720037247467,1,132),
('2022-06-01 12:00:23',589402514225,0,133),
('2022-06-01 12:38:15',589402514225,1,134),
('2022-06-01 13:41:14',45336916925,1,135),
('2022-06-01 16:46:22',45336916925,0,136),
('2022-06-01 16:48:00',589402514225,0,137),
('2022-06-02 07:53:28',45336916925,1,138),
('2022-06-02 07:57:28',589402514225,1,139),
('2022-06-02 10:02:33',720037247467,1,140),
('2022-06-02 12:00:36',589402514225,0,141),
('2022-06-02 12:00:49',720037247467,0,142),
('2022-06-02 12:00:58',45336916925,0,143),
('2022-06-02 12:37:32',589402514225,1,144),
('2022-06-02 12:48:43',720037247467,1,145),
('2022-06-02 12:48:56',45336916925,1,146),
('2022-06-02 16:23:55',589402514225,0,147),
('2022-06-03 07:58:50',589402514225,1,148),
('2022-06-03 08:01:50',45336916925,1,149),
('2022-06-03 12:00:19',589402514225,0,150),
('2022-06-03 12:01:09',45336916925,0,151),
('2022-06-03 12:39:24',589402514225,1,152),
('2022-06-03 12:48:16',45336916925,1,153),
('2022-06-03 16:47:11',589402514225,0,154),
('2022-06-03 16:49:45',45336916925,0,155),
('2022-06-07 07:52:43',589402514225,1,156),
('2022-06-07 09:08:10',720037247467,1,157),
('2022-06-07 12:00:49',589402514225,0,158),
('2022-06-07 12:36:03',589402514225,1,159),
('2022-06-07 12:48:14',45336916925,1,160),
('2022-06-07 16:47:30',720037247467,0,161),
('2022-06-07 16:47:32',589402514225,0,162),
('2022-06-07 16:48:04',45336916925,0,163),
('2022-06-08 07:56:43',589402514225,1,164),
('2022-06-08 07:57:05',45336916925,1,165),
('2022-06-08 09:28:26',720037247467,1,166),
('2022-07-13 09:27:50',589402514225,1,167),
('2022-07-13 09:28:06',589402514225,0,168),
('2022-09-06 10:25:14',589402514225,1,221),
('2022-09-06 10:29:34',589402514225,1,226),
('2022-09-06 10:29:43',589402514225,0,231),
('2022-09-06 10:34:55',42,1,236),
('2022-09-13 10:29:07',42,0,237);
UNLOCK TABLES;
