-- when galera was use
DELIMITER //
CREATE PROCEDURE `insert_log`(id_badge bigint, inside bool) 
 MODIFIES SQL DATA
BEGIN
    IF (SELECT VARIABLE_VALUE FROM information_schema.GLOBAL_STATUS 
        WHERE VARIABLE_NAME='wsrep_ready') = 'on'
    THEN
        INSERT INTO `log_write` (`date`, `id_badge`, `inside` ) VALUES (NOW(), id_badge, inside);
        CALL `insert_log_sync`;
    ELSE
        CALL `insert_log_write_force`(id_badge, inside);
    END IF;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE `insert_log_sync`()
    MODIFIES SQL DATA
BEGIN
    INSERT INTO `log_sync` (`date`, `id_badge`, `inside`) 
    (
        SELECT `date`, `id_badge`, `inside` FROM `log_write` 
        WHERE (`date`, `id_badge`, `inside`) NOT IN (SELECT `date`, `id_badge`, `inside` FROM `log_sync`)
    );
    CALL `delete_log_write`;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE `insert_log_write_force`(id_badge bigint, inside bool) 
 MODIFIES SQL DATA
BEGIN
    SET GLOBAL wsrep_on=off;
    INSERT INTO `log_write` (`date`, `id_badge`, `inside` ) VALUES (NOW(), id_badge, inside);
    SET GLOBAL wsrep_on=on;
END //
DELIMITER ;

CREATE PROCEDURE `delete_log_write`()
    MODIFIES SQL DATA
        DELETE FROM `log_write` 
        WHERE (`date`, `id_badge`, `inside`) IN 
        (
            SELECT `date`, `id_badge`, `inside` FROM `log_sync`
        );







DELIMITER //
CREATE PROCEDURE `insert_badge`(id_badge bigint, id_user int) 
 MODIFIES SQL DATA
BEGIN
    IF (SELECT VARIABLE_VALUE FROM information_schema.GLOBAL_STATUS 
        WHERE VARIABLE_NAME='wsrep_ready') = 'on'
    THEN
        INSERT INTO `badge_write` (`id_badge`, `id_user`) VALUES (id_badge, id_user);
        CALL `insert_badge_sync`;
    ELSE
        CALL `insert_badge_write_force`(id_badge, id_user);
    END IF;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE `insert_badge_sync`()
    MODIFIES SQL DATA
BEGIN
    INSERT INTO `badge_sync` (`id_badge`, `id_user`) 
    (
        SELECT `id_badge`, `id_user` FROM `badge_write` 
        WHERE (`id_badge`, `id_user`) NOT IN (SELECT  `id_badge`, `id_user` FROM `badge_sync`)
    );
    CALL `delete_badge_write`;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE `insert_badge_write_force`(id_badge bigint, id_user int) 
 MODIFIES SQL DATA
BEGIN
    SET GLOBAL wsrep_on=off;
    INSERT INTO `badge_write` (`id_badge`, `id_user` ) VALUES (id_badge, id_user);
    SET GLOBAL wsrep_on=on;
END //
DELIMITER ;

CREATE PROCEDURE `delete_badge_write`()
    MODIFIES SQL DATA
        DELETE FROM `badge_write` 
        WHERE (`id_badge`, `id_user`) IN 
        (
            SELECT `id_badge`, `id_user` FROM `badge_sync`
        );





DELIMITER //
CREATE PROCEDURE `insert_user`(name text, surname text) 
 MODIFIES SQL DATA
BEGIN
    IF (SELECT VARIABLE_VALUE FROM information_schema.GLOBAL_STATUS 
        WHERE VARIABLE_NAME='wsrep_ready') = 'on'
    THEN
        INSERT INTO `user_write` (`name`, `surname`) VALUES (name, surname);
        CALL `insert_user_sync`;
    ELSE
        CALL `insert_user_write_force`(name, surname);
    END IF;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE `insert_user_sync`()
    MODIFIES SQL DATA
BEGIN
    INSERT INTO `user_sync` (`name`, `surname`) 
    (
        SELECT `name`, `surname` FROM `user_write` 
        WHERE (`name`, `surname`) NOT IN (SELECT  `name`, `surname` FROM `user_sync`)
    );
    CALL `delete_user_write`;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE `insert_user_write_force`(name text, surname text) 
 MODIFIES SQL DATA
BEGIN
    SET GLOBAL wsrep_on=off;
    INSERT INTO `user_write` (`name`, `surname` ) VALUES (name, surname);
    SET GLOBAL wsrep_on=on;
END //
DELIMITER ;

CREATE PROCEDURE `delete_user_write`()
    MODIFIES SQL DATA
        DELETE FROM `user_write` 
        WHERE (`name`, `surname`) IN 
        (
            SELECT `name`, `surname` FROM `user_sync`
        );

