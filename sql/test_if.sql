DELIMITER //
DROP PROCEDURE IF EXISTS `test_if`; 
CREATE PROCEDURE `test_if`()
BEGIN
    IF 1 = (SELECT 2) THEN
        SELECT 1;
    ELSEIF 1 = (SELECT 1) THEN
        SELECT 'else if';
    ELSE
        SELECT 'else';
    END IF;
END //
DELIMITER;

CALL `test_if`;