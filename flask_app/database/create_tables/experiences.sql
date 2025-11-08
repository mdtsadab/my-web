CREATE TABLE IF NOT EXISTS `experiences` (
  `experience_id`   int(11)      NOT NULL AUTO_INCREMENT COMMENT 'The experience id',
  `position_id`     int(11)      NOT NULL                COMMENT 'FK:The position id',
  `name`            varchar(200) NOT NULL                COMMENT 'The name of the experience',
  `description`     TEXT         NOT NULL                COMMENT 'Description of the experience',
  `hyperlink`       varchar(100) DEFAULT NULL            COMMENT 'Hyperlink to more info',
  `start_date`      date         DEFAULT NULL            COMMENT 'Start date of experience',
  `end_date`        date         DEFAULT NULL            COMMENT 'End date of experience',
  PRIMARY KEY (`experience_id`),
  FOREIGN KEY (`position_id`) REFERENCES positions(`position_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT="Experiences I have had";