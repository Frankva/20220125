-- rewrite when galera is not used.
CREATE PROCEDURE `delete_log_write`()
    MODIFIES SQL DATA
        DELETE FROM `log_write` 
        WHERE (`date`, `id_badge`, `inside`) IN 
        (
            SELECT `date`, `id_badge`, `inside` FROM `log_sync`
        );

DELIMITER //
CREATE PROCEDURE `insert_log`(id_badge bigint, inside bool) 
 MODIFIES SQL DATA
BEGIN
    INSERT INTO `log_write` (`date`, `id_badge`, `inside` ) VALUES (NOW(),
        id_badge, inside);
    CALL `delete_log_write`;
END //
DELIMITER ;

CREATE PROCEDURE `get_unsync_log`()
        SELECT `date`, `id_badge`, `inside`
        FROM `log_write`
        WHERE (`date`, `id_badge`, `inside`)
        NOT IN (SELECT `date`, `id_badge`, `inside` FROM `log_sync`);


CREATE PROCEDURE `delete_badge_write`()
    MODIFIES SQL DATA
        DELETE FROM `badge_write` 
        WHERE (`id_badge`, `id_user`) IN 
        (
            SELECT `id_badge`, `id_user` FROM `badge_sync`
        );

DELIMITER //
CREATE PROCEDURE `insert_badge`(id_badge bigint, id_user int) 
 MODIFIES SQL DATA
BEGIN
    INSERT INTO `badge_write` (`id_badge`, `id_user`) VALUES (id_badge, id_user);
    CALL `delete_badge_write`;
END //
DELIMITER ;





CREATE PROCEDURE `delete_user_write`()
    MODIFIES SQL DATA
        DELETE FROM `user_write` 
        WHERE (`name`, `surname`) IN 
        (
            SELECT `name`, `surname` FROM `user_sync`
        );

DELIMITER //
CREATE PROCEDURE `insert_user`(name text, surname text) 
 MODIFIES SQL DATA
BEGIN
        INSERT INTO `user_write` (`name`, `surname`) VALUES (name, surname);
        CALL `delete_user_write`;
END //
DELIMITER ;


