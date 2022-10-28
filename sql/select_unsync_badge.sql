SELECT `id_badge`, `name`, `surname`
FROM `badge_write` LEFT OUTER JOIN `user_write`
ON `badge_write`.`id_user` = `user_write`.`id_user`
WHERE `id_badge`
NOT IN (SELECT `id_badge` FROM `badge_sync`);