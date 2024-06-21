-- u1500184_vk_bot.vk_group определение

CREATE TABLE IF NOT EXIST vk_group (
  vk_group_id varchar(20) NOT NULL,
  group_name varchar(50) DEFAULT NULL,
  privileges json DEFAULT NULL,
  PRIMARY KEY (vk_group_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- u1500184_vk_bot.vk_user определение

CREATE TABLE IF NOT EXIST vk_user (
  vk_user_id varchar(20) NOT NULL,
  first_name varchar(30) DEFAULT NULL,
  last_name varchar(30) DEFAULT NULL,
  photo_link varchar(300) DEFAULT NULL,
  PRIMARY KEY (vk_user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- u1500184_vk_bot.note определение

CREATE TABLE IF NOT EXIST note (
  group_id varchar(20) NOT NULL,
  owner_id varchar(20) NOT NULL,
  note_id int(11) NOT NULL AUTO_INCREMENT,
  header varchar(100) NOT NULL,
  description text NOT NULL,
  addition_date datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  modified_date datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (note_id),
  UNIQUE KEY unique_note (group_id, owner_id, note_id),
  KEY group_id (group_id),
  KEY owner_id (owner_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- u1500184_vk_bot.user_group определение

CREATE TABLE IF NOT EXIST user_group (
  vk_user_id varchar(20) NOT NULL,
  vk_group_id varchar(20) NOT NULL,
  is_admin tinyint(1) NOT NULL,
  UNIQUE KEY vk_user_group (vk_user_id, vk_group_id),
  KEY group_key (vk_group_id),
  CONSTRAINT fk_group FOREIGN KEY (vk_group_id) REFERENCES vk_group (vk_group_id) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_user FOREIGN KEY (vk_user_id) REFERENCES vk_user (vk_user_id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- u1500184_vk_bot.vk_user_token определение

CREATE TABLE IF NOT EXIST vk_user_token (
  vk_user_id varchar(20) NOT NULL,
  token varchar(150) NOT NULL,
  last_date datetime NOT NULL,
  PRIMARY KEY (token),
  KEY user_key (vk_user_id),
  CONSTRAINT fk_user FOREIGN KEY (vk_user_id) REFERENCES vk_user (vk_user_id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
