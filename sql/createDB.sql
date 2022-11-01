-- CREATE DATABASE `timbreuse2022`;
CREATE DATABASE `db20221101081819`;
-- USE `timbreuse2022`;
USE `db20221101081819`;
CREATE TABLE `user_sync` ( `id_user` int(11) NOT NULL, `name` text COLLATE utf8mb4_unicode_ci NOT NULL, `surname` text COLLATE utf8mb4_unicode_ci NOT NULL, PRIMARY KEY (`id_user`)) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;
CREATE TABLE `user_write` ( `id_user` int(11) NOT NULL AUTO_INCREMENT, `name` text COLLATE utf8mb4_unicode_ci NOT NULL, `surname` text COLLATE utf8mb4_unicode_ci NOT NULL, PRIMARY KEY (`id_user`)) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;
CREATE TABLE `badge_sync` ( `id_badge` bigint(20) NOT NULL, `id_user` int(11) NOT NULL, PRIMARY KEY (`id_badge`), FOREIGN KEY (`id_user`) REFERENCES `user_sync` (`id_user`)) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;
CREATE TABLE `badge_write` ( `id_badge` bigint(20) NOT NULL, `id_user` int(11) NOT NULL, PRIMARY KEY (`id_badge`)) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;
CREATE TABLE `log_sync` ( `date` datetime NOT NULL, `id_badge` bigint(20) NOT NULL, `inside` tinyint(1) NOT NULL, `id_log` int(11) NOT NULL, PRIMARY KEY (`id_log`), FOREIGN KEY (`id_badge`) REFERENCES `badge_sync` (`id_badge`)) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;
CREATE TABLE `log_write` ( `date` datetime NOT NULL DEFAULT NOW(), `id_badge` bigint(20) NOT NULL, `inside` tinyint(1) NOT NULL, `id_log` int(11) NOT NULL AUTO_INCREMENT, PRIMARY KEY (`id_log`)) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;
CREATE VIEW `user` AS SELECT * FROM `user_sync` UNION SELECT * FROM `user_write` WHERE (`name`, `surname`) NOT IN ( SELECT `name`, `surname` FROM `user_sync`) ORDER BY `NAME`;
CREATE VIEW `badge` AS SELECT * FROM `badge_sync` UNION SELECT * FROM `badge_write` WHERE (`id_badge`, `id_user`) NOT IN ( SELECT `id_badge`, `id_user` FROM `badge_sync`);
CREATE VIEW `log` AS SELECT * FROM `log_sync` UNION SELECT * FROM `log_write` WHERE (`date`, `id_badge`, `inside`) NOT IN ( SELECT `date`, `id_badge`, `inside` FROM `log_sync`) ORDER BY `DATE`;
CREATE PROCEDURE `delete_log_write`() MODIFIES SQL DATA DELETE FROM `log_write` WHERE (`date`, `id_badge`, `inside`) IN ( SELECT `date`, `id_badge`, `inside` FROM `log_sync`);
DELIMITER // CREATE PROCEDURE `insert_log`(id_badge bigint, inside bool) MODIFIES SQL DATA BEGIN INSERT INTO `log_write` (`date`, `id_badge`, `inside` ) VALUES (NOW(), id_badge, inside); CALL `delete_log_write`; END // DELIMITER ;
DELIMITER // DROP PROCEDURE IF EXISTS `insert_sync_log`; CREATE PROCEDURE `insert_sync_log`(_date DATETIME, id_badge BIGINT, inside BOOL, id_log INT) MODIFIES SQL DATA BEGIN INSERT INTO `log_sync` (`date`, `id_badge`, `inside`, `id_log`) VALUES (_date, id_badge, inside, id_log); CALL `delete_log_write`; END // DELIMITER ;
CREATE PROCEDURE `delete_badge_write`() MODIFIES SQL DATA DELETE FROM `badge_write` WHERE `id_badge` IN ( SELECT `id_badge` FROM `badge_sync`);
DELIMITER // CREATE PROCEDURE `insert_badge`(id_badge BIGINT, id_user INT) MODIFIES SQL DATA BEGIN INSERT INTO `badge_write` (`id_badge`, `id_user`) VALUES (id_badge, id_user); CALL `delete_badge_write`; END // DELIMITER ;
CREATE PROCEDURE `delete_user_write`() MODIFIES SQL DATA DELETE FROM `user_write` WHERE (`name`, `surname`) IN ( SELECT `name`, `surname` FROM `user_sync`);
DELIMITER // CREATE PROCEDURE `insert_user`(_name TEXT, surname TEXT) MODIFIES SQL DATA BEGIN INSERT INTO `user_write` (`name`, `surname`) VALUES (_name, surname); CALL `delete_user_write`; END // DELIMITER ;
DELIMITER // CREATE PROCEDURE `insert_users_and_badges`(id_badge BIGINT, id_user INT, _name TEXT, surname TEXT) MODIFIES SQL DATA BEGIN DECLARE EXIT HANDLER FOR SQLEXCEPTION BEGIN ROLLBACK; END; START TRANSACTION; INSERT INTO `user_sync` (`id_user`, `name`, `surname`) VALUES (id_user, _name, surname); INSERT INTO `badge_sync` (`id_badge`, `id_user`) VALUES (id_badge, id_user); COMMIT; CALL `delete_user_write`; CALL `delete_badge_write`; END // DELIMITER ;