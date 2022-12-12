CREATE DATABASE `tmp`;
USE `tmp`;
-- CREATE DATABASE `timbreuse2022`;
-- USE `timbreuse2022`;
CREATE TABLE `user_sync` ( `id_user` int(11) NOT NULL, `name` text COLLATE utf8mb4_unicode_ci NOT NULL, `surname` text COLLATE utf8mb4_unicode_ci NOT NULL, PRIMARY KEY (`id_user`)) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;
CREATE TABLE `user_write` ( `id_user` int(11) NOT NULL AUTO_INCREMENT, `name` text COLLATE utf8mb4_unicode_ci NOT NULL, `surname` text COLLATE utf8mb4_unicode_ci NOT NULL, PRIMARY KEY (`id_user`)) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;
CREATE TABLE `badge_sync` ( `id_badge` bigint(20) NOT NULL, `id_user` int(11), `rowid_badge` int(11) UNIQUE NOT NULL, PRIMARY KEY (`id_badge`), FOREIGN KEY (`id_user`) REFERENCES `user_sync` (`id_user`)) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;
CREATE TABLE `badge_write` ( `id_badge` bigint(20) NOT NULL, `id_user` int(11) NOT NULL, PRIMARY KEY (`id_badge`)) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;
CREATE TABLE `log_sync` ( `date` datetime NOT NULL, `id_badge` bigint(20), `inside` tinyint(1) NOT NULL, `id_log` int(11) NOT NULL, `id_user` int(11) NOT NULL, `date_badge` datetime, `date_modif` datetime NOT NULL, `date_delete` datetime, PRIMARY KEY (`id_log`), FOREIGN KEY (`id_badge`) REFERENCES `badge_sync` (`id_badge`), FOREIGN KEY (`id_user`) REFERENCES `user_sync` (`id_user`)) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;
CREATE TABLE `log_write` ( `date` datetime NOT NULL DEFAULT NOW(), `id_badge` bigint(20) NOT NULL, `inside` tinyint(1) NOT NULL, `id_log` int(11) NOT NULL AUTO_INCREMENT, PRIMARY KEY (`id_log`)) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;
DROP VIEW IF EXISTS `user`;
CREATE VIEW `user` AS SELECT * FROM `user_sync` UNION SELECT * FROM `user_write` WHERE (`name`, `surname`) NOT IN ( SELECT `name`, `surname` FROM `user_sync`) ORDER BY `NAME`;
DROP VIEW IF EXISTS `badge`;
CREATE VIEW `badge` AS SELECT `id_badge`, `id_user` FROM `badge_sync` UNION SELECT * FROM `badge_write` WHERE `id_badge` NOT IN ( SELECT `id_badge` FROM `badge_sync`) ; 
DROP VIEW IF EXISTS `log`;
CREATE VIEW `log` AS SELECT `date`, `id_badge`, `inside`, `id_log`, `id_user` FROM `log_sync` UNION SELECT `date`, `log_write`.`id_badge`, `inside`, `id_log`, `id_user` FROM `log_write` LEFT OUTER JOIN `badge` ON `log_write`.`id_badge` = `badge`.`id_badge` WHERE ( `date`, `log_write`.`id_badge`, `inside`) NOT IN ( SELECT `date`, `id_badge`, `inside` FROM `log_sync`) ORDER BY `date`; 
CREATE PROCEDURE `delete_log_write`() MODIFIES SQL DATA DELETE FROM `log_write` WHERE (`date`, `id_badge`, `inside`) IN ( SELECT `date`, `id_badge`, `inside` FROM `log_sync`);
CREATE PROCEDURE `insert_log`(id_badge BIGINT, inside BOOL) MODIFIES SQL DATA BEGIN INSERT INTO `log_write` (`date`, `id_badge`, `inside` ) VALUES (NOW(), id_badge, inside); CALL `delete_log_write`; END;
CREATE PROCEDURE `insert_sync_log`(_date DATETIME, id_badge BIGINT, inside BOOL, id_log INT, id_user INT) MODIFIES SQL DATA BEGIN INSERT INTO `log_sync` (`date`, `id_badge`, `inside`, `id_log`, `id_user`) VALUES (_date, id_badge, inside, id_log, id_user); CALL `delete_log_write`; END;
CREATE PROCEDURE `delete_badge_write`() MODIFIES SQL DATA DELETE FROM `badge_write` WHERE `id_badge` IN ( SELECT `id_badge` FROM `badge_sync`);
CREATE PROCEDURE `insert_badge`(id_badge BIGINT, id_user INT) MODIFIES SQL DATA BEGIN INSERT INTO `badge_write` (`id_badge`, `id_user`) VALUES (id_badge, id_user); CALL `delete_badge_write`; END;
CREATE PROCEDURE `delete_user_write`() MODIFIES SQL DATA DELETE FROM `user_write` WHERE (`name`, `surname`) IN ( SELECT `name`, `surname` FROM `user_sync`);
CREATE PROCEDURE `insert_user`(_name TEXT, surname TEXT) MODIFIES SQL DATA BEGIN INSERT INTO `user_write` (`name`, `surname`) VALUES (_name, surname); CALL `delete_user_write`; END;
CREATE PROCEDURE `insert_users_and_badges`(id_badge BIGINT, id_user INT, _name TEXT, surname TEXT) MODIFIES SQL DATA BEGIN DECLARE EXIT HANDLER FOR SQLEXCEPTION BEGIN ROLLBACK; END; START TRANSACTION; INSERT INTO `user_sync` (`id_user`, `name`, `surname`) VALUES (id_user, _name, surname); INSERT INTO `badge_sync` (`id_badge`, `id_user`) VALUES (id_badge, id_user); COMMIT; CALL `delete_user_write`; CALL `delete_badge_write`; END;
-- new not tested
CREATE PROCEDURE `insert_user_sync`(_id_user INT, _name TEXT, _surname TEXT) MODIFIES SQL DATA BEGIN INSERT INTO `user_sync` (`id_user`, `name`, `surname`) VALUES (_id_user, _name, _surname); CALL `delete_user_write`; END;
CREATE PROCEDURE `insert_badge_sync` (_id_badge BIGINT, _id_user INT, _rowid_badge INT) MODIFIES SQL DATA BEGIN INSERT INTO `badge_sync` (`id_badge`, `id_user`, `rowid_badge`) VALUES (_id_badge, _id_user, _rowid_badge); CALL `delete_badge_write`; END;
-- true

-- DELIMITER // CREATE PROCEDURE `insert_log`(id_badge BIGINT, inside BOOL) MODIFIES SQL DATA BEGIN INSERT INTO `log_write` (`date`, `id_badge`, `inside` ) VALUES (NOW(), id_badge, inside); CALL `delete_log_write`; END // DELIMITER ;
-- DELIMITER // DROP PROCEDURE IF EXISTS `insert_sync_log`; CREATE PROCEDURE `insert_sync_log`(_date DATETIME, id_badge BIGINT, inside BOOL, id_log INT, id_user INT) MODIFIES SQL DATA BEGIN INSERT INTO `log_sync` (`date`, `id_badge`, `inside`, `id_log`, `id_user`) VALUES (_date, id_badge, inside, id_log, id_user); CALL `delete_log_write`; END // DELIMITER ;
-- CREATE PROCEDURE `delete_badge_write`() MODIFIES SQL DATA DELETE FROM `badge_write` WHERE `id_badge` IN ( SELECT `id_badge` FROM `badge_sync`);
-- DELIMITER // CREATE PROCEDURE `insert_badge`(id_badge BIGINT, id_user INT) MODIFIES SQL DATA BEGIN INSERT INTO `badge_write` (`id_badge`, `id_user`) VALUES (id_badge, id_user); CALL `delete_badge_write`; END // DELIMITER ;
-- CREATE PROCEDURE `delete_user_write`() MODIFIES SQL DATA DELETE FROM `user_write` WHERE (`name`, `surname`) IN ( SELECT `name`, `surname` FROM `user_sync`);
-- DELIMITER // CREATE PROCEDURE `insert_user`(_name TEXT, surname TEXT) MODIFIES SQL DATA BEGIN INSERT INTO `user_write` (`name`, `surname`) VALUES (_name, surname); CALL `delete_user_write`; END // DELIMITER ;
-- DELIMITER // CREATE PROCEDURE `insert_users_and_badges`(id_badge BIGINT, id_user INT, _name TEXT, surname TEXT) MODIFIES SQL DATA BEGIN DECLARE EXIT HANDLER FOR SQLEXCEPTION BEGIN ROLLBACK; END; START TRANSACTION; INSERT INTO `user_sync` (`id_user`, `name`, `surname`) VALUES (id_user, _name, surname); INSERT INTO `badge_sync` (`id_badge`, `id_user`) VALUES (id_badge, id_user); COMMIT; CALL `delete_user_write`; CALL `delete_badge_write`; END // DELIMITER ;