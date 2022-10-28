-- rewrite when galera is not used.
DROP PROCEDURE IF EXISTS `delete_log_write`;
CREATE PROCEDURE `delete_log_write`()
    MODIFIES SQL DATA
        DELETE FROM `log_write` 
        WHERE (`date`, `id_badge`, `inside`) IN 
        (
            SELECT `date`, `id_badge`, `inside` FROM `log_sync`
        );

DELIMITER //

DROP PROCEDURE IF EXISTS `insert_log`;
CREATE PROCEDURE `insert_log`(id_badge bigint, inside bool) 
 MODIFIES SQL DATA
BEGIN
    INSERT INTO `log_write` (`date`, `id_badge`, `inside` ) VALUES (NOW(),
        id_badge, inside);
    CALL `delete_log_write`;
END //
DELIMITER ;

DELIMITER //

DROP PROCEDURE IF EXISTS `insert_sync_log`;
CREATE PROCEDURE `insert_sync_log`(_date DATETIME, id_badge BIGINT,
    inside BOOL, id_log INT) 
 MODIFIES SQL DATA
BEGIN
    INSERT INTO `log_sync` (`date`, `id_badge`, `inside`, `id_log`) VALUES
    (_date, id_badge, inside, id_log);
    -- to be optimize
    CALL `delete_log_write`;
END //
DELIMITER ;

-- CREATE PROCEDURE `get_unsync_log`()
--         SELECT `date`, `id_badge`, `inside`
--         FROM `log_write`
--         WHERE (`date`, `id_badge`, `inside`)
--         NOT IN (SELECT `date`, `id_badge`, `inside` FROM `log_sync`);
--     
-- call `get_unsync_log`;


DROP PROCEDURE IF EXISTS `delete_badge_write`;
CREATE PROCEDURE `delete_badge_write`()
    MODIFIES SQL DATA
        DELETE FROM `badge_write` 
        WHERE `id_badge` IN 
        (
            SELECT `id_badge` FROM `badge_sync`
        );

DROP PROCEDURE IF EXISTS `insert_badge`;
DELIMITER //
CREATE PROCEDURE `insert_badge`(id_badge BIGINT, id_user INT) 
 MODIFIES SQL DATA
BEGIN
    INSERT INTO `badge_write` (`id_badge`, `id_user`) VALUES (id_badge, id_user);
    CALL `delete_badge_write`;
END //
DELIMITER ;





DROP PROCEDURE IF EXISTS `delete_user_write`;
CREATE PROCEDURE `delete_user_write`()
    MODIFIES SQL DATA
        DELETE FROM `user_write` 
        WHERE (`name`, `surname`) IN 
        (
            SELECT `name`, `surname` FROM `user_sync`
        );


DROP PROCEDURE IF EXISTS `insert_user`;
DELIMITER //
CREATE PROCEDURE `insert_user`(_name TEXT, surname TEXT) 
 MODIFIES SQL DATA
BEGIN
        INSERT INTO `user_write` (`name`, `surname`) VALUES (_name, surname);
        CALL `delete_user_write`;
END //
DELIMITER ;


DROP PROCEDURE IF EXISTS `insert_users_and_badges`;
DELIMITER //
CREATE PROCEDURE `insert_users_and_badges`(id_badge BIGINT, id_user INT,
    _name TEXT, surname TEXT) 
 MODIFIES SQL DATA
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
    END;
    START TRANSACTION;
    INSERT INTO `user_sync` (`id_user`, `name`, `surname`)
    VALUES (id_user, _name, surname);
    INSERT INTO `badge_sync` (`id_badge`, `id_user`)
    VALUES (id_badge, id_user);
    COMMIT;

    -- can be better to optimize
    CALL `delete_user_write`;
    CALL `delete_badge_write`;
END //
DELIMITER ;

CALL `insert_users_and_badges`(42);


