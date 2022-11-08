-- log view is log_sync and log_write combine (with a union); log_write take
-- the user id of the badge view (badge_sync+badge_write) with a join
-- this script is in createDB.sql
DROP VIEW IF EXISTS `log`;

CREATE VIEW `log` AS 
	SELECT *
	FROM `log_sync`
	UNION
	SELECT `date`, `log_write`.`id_badge`, `inside`, `id_log`, `id_user`
	FROM `log_write`
	    LEFT OUTER JOIN `badge` ON `log_write`.`id_badge` = `badge`.`id_badge`
	WHERE (
	        `date`, `log_write`.`id_badge`, `inside`
	    ) NOT IN (
	        SELECT `date`, `id_badge`, `inside`
	        FROM `log_sync`
	    )
	ORDER BY `DATE`; 