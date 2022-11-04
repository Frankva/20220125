START TRANSACTION;

DELIMITER //
FOR user_id IN (
    SELECT `id_user`
    FROM `user_sync`
)
DO
     UPDATE `log_sync`
     SET `id_user` = user_id
     WHERE `id_badge` IN (
             SELECT `id_badge`
             FROM `badge_sync`
             WHERE `id_user` = user_id
         );

END FOR;
//
DELIMITER;

ROLLBACK;
----------------
START TRANSACTION;
UPDATE `log_sync`
SET `id_user` = 8
WHERE `id_badge` IN (
    SELECT `id_badge`
    FROM `badge_sync`
    WHERE `id_user` = 8
);
UPDATE `log_sync`
SET `id_user` = 92
WHERE `id_badge` IN (
    SELECT `id_badge`
    FROM `badge_sync`
    WHERE `id_user` = 92
);
UPDATE `log_sync`
SET `id_user` = 93
WHERE `id_badge` IN (
    SELECT `id_badge`
    FROM `badge_sync`
    WHERE `id_user` = 93
);
UPDATE `log_sync`
SET `id_user` = 94
WHERE `id_badge` IN (
    SELECT `id_badge`
    FROM `badge_sync`
    WHERE `id_user` = 94
);
UPDATE `log_sync`
SET `id_user` = 95
WHERE `id_badge` IN (
    SELECT `id_badge`
    FROM `badge_sync`
    WHERE `id_user` = 95
);
UPDATE `log_sync`
SET `id_user` = 96
WHERE `id_badge` IN (
    SELECT `id_badge`
    FROM `badge_sync`
    WHERE `id_user` = 96
);
UPDATE `log_sync`
SET `id_user` = 97
WHERE `id_badge` IN (
    SELECT `id_badge`
    FROM `badge_sync`
    WHERE `id_user` = 97
);
UPDATE `log_sync`
SET `id_user` = 98
WHERE `id_badge` IN (
    SELECT `id_badge`
    FROM `badge_sync`
    WHERE `id_user` = 98
);
UPDATE `log_sync`
SET `id_user` = 106
WHERE `id_badge` IN (
    SELECT `id_badge`
    FROM `badge_sync`
    WHERE `id_user` = 106
);
UPDATE `log_sync`
SET `id_user` = 107
WHERE `id_badge` IN (
    SELECT `id_badge`
    FROM `badge_sync`
    WHERE `id_user` = 107
);
UPDATE `log_sync`
SET `id_user` = 108
WHERE `id_badge` IN (
    SELECT `id_badge`
    FROM `badge_sync`
    WHERE `id_user` = 108
);
UPDATE `log_sync`
SET `id_user` = 109
WHERE `id_badge` IN (
    SELECT `id_badge`
    FROM `badge_sync`
    WHERE `id_user` = 109
);
UPDATE `log_sync`
SET `id_user` = 110
WHERE `id_badge` IN (
    SELECT `id_badge`
    FROM `badge_sync`
    WHERE `id_user` = 110
);
UPDATE `log_sync`
SET `id_user` = 111
WHERE `id_badge` IN (
    SELECT `id_badge`
    FROM `badge_sync`
    WHERE `id_user` = 111
);
COMMIT;
ROLLBACK;