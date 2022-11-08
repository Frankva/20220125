-- ALTER TABLE `badge_sync`
-- DROP CONSTRAINT badge_sync_ibfk_1;

-- remove not null and unique key
SHOW CREATE TABLE `badge_sync`;
START TRANSACTION;
ALTER TABLE `badge_sync`
CHANGE `id_user` `id_user` int(11);
ROLLBACK;

START TRANSACTION;
ALTER TABLE `badge_sync`
DROP UNIQUE KEY ;

ROLLBACK;

START TRANSACTION;
ALTER TABLE `badge_sync`
DROP CONSTRAINT `id_user`;
ROLLBACK;


START TRANSACTION;
ALTER TABLE `badge_sync`
ADD FOREIGN KEY (`id_user`) REFERENCES `user_sync` (`id_user`);

ROLLBACK;


COMMIT;