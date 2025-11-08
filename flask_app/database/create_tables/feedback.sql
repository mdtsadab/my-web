CREATE TABLE IF NOT EXISTS `feedback` (
  `feedback_id`  int(11)       NOT NULL AUTO_INCREMENT COMMENT 'The feedback id',
  `name`         varchar(100)  NOT NULL                COMMENT 'Name of submitter',
  `email`        varchar(100)  NOT NULL                COMMENT 'Email of submitter',
  `message`      varchar(500)  NOT NULL                COMMENT 'Feedback message',
  `submitted_at` datetime      DEFAULT CURRENT_TIMESTAMP COMMENT 'Submission timestamp',
  PRIMARY KEY (`feedback_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT="User feedback submissions";