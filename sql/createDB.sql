CREATE DATABASE `timbreuse2022`;
USE `timbreuse2022`;
CREATE TABLE `user` ( `id_user` int(11) NOT NULL AUTO_INCREMENT, `name` text NOT NULL, `surname` text NOT NULL, PRIMARY KEY (`id_user`)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
CREATE TABLE `badge` ( `id_badge` bigint(20) NOT NULL, `id_user` int(11) NOT NULL, PRIMARY KEY (`id_badge`), FOREIGN KEY (`id_user`) REFERENCES `user` (`id_user`)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
CREATE TABLE `log` ( `date` datetime NOT NULL DEFAULT NOW(), `id_badge` bigint(20) NOT NULL, `inside` tinyint(1) NOT NULL, id_log int NOT NULL AUTO_INCREMENT, PRIMARY KEY (`id_log`), FOREIGN KEY (`id_badge`) REFERENCES `badge` (`id_badge`)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
COMMIT;