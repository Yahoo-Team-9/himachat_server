USE himachat;

CREATE TABLE users(
	primary_user_id INT(9) PRIMARY KEY AUTO_INCREMENT,
	user_id VARCHAR(64) NOT NULL,
	user_name VARCHAR(64) NOT NULL,
	user_image_pass varchar(128),
	bio varchar(256),
	login_at DATETIME default current_timestamp,
	created_at DATETIME default current_timestamp,
	updated_at DATETIME default current_timestamp on update current_timestamp,
	delete_flg BOOLEAN DEFAULT 0,
	hima BOOLEAN DEFAULT 1
);

CREATE TABLE social_login_users(
    social_login_id INT(9) PRIMARY KEY AUTO_INCREMENT,
    primary_user_id INT(9) ,
    email VARCHAR(128) NOT NULL,
    provider_name VARCHAR(64) NOT NULL,
    created_at DATETIME default current_timestamp,
	updated_at DATETIME default current_timestamp on update current_timestamp,
	delete_flg BOOLEAN DEFAULT 0,
	FOREIGN KEY(primary_user_id)
	REFERENCES users(primary_user_id)
);

CREATE TABLE secret_user_sessions(
    primary_id INT(12) PRIMARY KEY AUTO_INCREMENT,
    primary_user_id INT(9) NOT NULL,
    secret_id VARCHAR(64) NOT NULL,
    used_flg BOOLEAN DEFAULT 0,
    created_at DATETIME default current_timestamp
);


CREATE TABLE server_hash
(
    primary_id INT(12) PRIMARY KEY AUTO_INCREMENT,
    secret_id VARCHAR(64) NOT NULL,
    used_flg BOOLEAN DEFAULT 0,
    created_at DATETIME default current_timestamp
);


CREATE TABLE user_groups(
	group_id INT(12) PRIMARY KEY AUTO_INCREMENT,
	group_owner INT(9),
	created_at DATETIME default current_timestamp,
	updated_at DATETIME default current_timestamp on update current_timestamp,
	delete_flg BOOLEAN DEFAULT 0,
	FOREIGN KEY(group_owner)
	REFERENCES users(primary_user_id)
);

CREATE TABLE group_users(
	group_user_id INT(12) PRIMARY KEY AUTO_INCREMENT,
	group_id INT(12),
	primary_user_id INT(9),
	created_at  DATETIME default current_timestamp,
	updated_at  DATETIME default current_timestamp on update current_timestamp,
	delete_flg BOOLEAN DEFAULT 0,
	FOREIGN KEY(primary_user_id)
	REFERENCES users(primary_user_id),
	FOREIGN KEY(group_id)
	REFERENCES user_groups(group_id)
);

CREATE TABLE chats(
	chat_id INT(12) PRIMARY KEY AUTO_INCREMENT,
	group_id INT(12),
	send_user INT(9),
	chat_type INT(1),
	created_at  DATETIME default current_timestamp,
	updated_at  DATETIME default current_timestamp on update current_timestamp,
	delete_flg BOOLEAN DEFAULT 0,	
	message varchar(10000),
	FOREIGN KEY(send_user)
	REFERENCES users(primary_user_id),
	FOREIGN KEY(group_id)
	REFERENCES user_groups(group_id)
);

CREATE TABLE friends(
	friend_id INT(12) PRIMARY KEY AUTO_INCREMENT,
	primary_user_id INT(9),
	friend INT(9),
	approval BOOLEAN DEFAULT 0,
	created_at  DATETIME default current_timestamp,
	updated_at  DATETIME default current_timestamp on update current_timestamp,
	delete_flg BOOLEAN DEFAULT 0,
	FOREIGN KEY(primary_user_id)
	REFERENCES users(primary_user_id),
	FOREIGN KEY(friend)
	REFERENCES users(primary_user_id)
);

CREATE TABLE customs(
	custom_id INT(12) PRIMARY KEY AUTO_INCREMENT,
	primary_user_id INT(9),
	custom_name VARCHAR(64),
	use_flg BOOLEAN DEFAULT 0,
	created_at  DATETIME default current_timestamp,
	updated_at  DATETIME default current_timestamp on update current_timestamp,
	delete_flg BOOLEAN DEFAULT 0,
	FOREIGN KEY(primary_user_id)
	REFERENCES users(primary_user_id)
);

CREATE TABLE custom_users(
	custom_user_id INT(12) PRIMARY KEY AUTO_INCREMENT,
	custom_id INT(12),
	allowed_user INT(9),
	created_at  DATETIME default current_timestamp,
	updated_at  DATETIME default current_timestamp on update current_timestamp,
	delete_flg BOOLEAN DEFAULT 0,
	FOREIGN KEY(custom_id)
	REFERENCES customs(custom_id),
	FOREIGN KEY(allowed_user)
	REFERENCES users(primary_user_id)
);

CREATE TABLE pull_notifications
(
    pull_notification_id INT(12) PRIMARY KEY AUTO_INCREMENT,
    notification_type    INT(1),
    notification_text    VARCHAR(256),
    primary_user_id      INT(9),
    partner_user_id      INT(9),
    in_read              BOOLEAN  DEFAULT 0,
    created_at           DATETIME default current_timestamp,
    updated_at           DATETIME default current_timestamp on update current_timestamp,
    delete_flg           BOOLEAN  DEFAULT 0,
    FOREIGN KEY (primary_user_id)
        REFERENCES users (primary_user_id),
    FOREIGN KEY (partner_user_id)
        REFERENCES users (primary_user_id)
);

CREATE TABLE tags(
	tag_id INT(9) PRIMARY KEY AUTO_INCREMENT,
	tag_name VARCHAR(64),
	created_at  DATETIME default current_timestamp,
	updated_at  DATETIME default current_timestamp on update current_timestamp,
	delete_flg BOOLEAN DEFAULT 0
);

CREATE TABLE user_tags(
	user_tag_id INT(12) PRIMARY KEY AUTO_INCREMENT,
	primary_user_id INT(9),
	tag_id INT(9),
	created_at  DATETIME default current_timestamp,
	updated_at  DATETIME default current_timestamp on update current_timestamp,
	delete_flg BOOLEAN DEFAULT 0,
	FOREIGN KEY(primary_user_id)
	REFERENCES users(primary_user_id),
	FOREIGN KEY(tag_id)
	REFERENCES tags(tag_id)
);



INSERT INTO users(user_id,user_name,user_image_pass,bio) VALUES("Shishamo_Love","????????????","./","????????????????????????????????????????????????????????????????????????????????????");
INSERT INTO users(user_id,user_name,user_image_pass,bio) VALUES("BGY32ff9weg","?????????","./","??????????????????????????????");
INSERT INTO users(user_id,user_name,user_image_pass,bio) VALUES("sawara_0325","?????????","./","?????????????????????????");
INSERT INTO users(user_id,user_name,user_image_pass,bio) VALUES("tuna532","?????????","./","7/2????????????????????????");
INSERT INTO users(user_id,user_name,user_image_pass,bio) VALUES("taidayo_","??????","./","?????????????????????????");
INSERT INTO users(user_id,user_name,user_image_pass,bio) VALUES("like_fugu_lile","??????","./","20???????????????????????????");
INSERT INTO users(user_id,user_name,user_image_pass,bio) VALUES("gcwu9e0hfeu","??????","./","??????????????????????");
INSERT INTO users(user_id,user_name,user_image_pass,bio) VALUES("ebi_0019","??????","./","????");
INSERT INTO users(user_id,user_name,user_image_pass,bio) VALUES("ji0h3fhjweuh02","????????????","./","?????????~");
INSERT INTO users(user_id,user_name,user_image_pass,bio) VALUES("8_oct","??????","./","???????????????????????????????????");

INSERT INTO friends(primary_user_id, friend, approval) VALUES(1, 2, 1);
INSERT INTO friends(primary_user_id, friend, approval) VALUES(2, 1, 1);
INSERT INTO friends(primary_user_id, friend, approval) VALUES(1, 3, 1);
INSERT INTO friends(primary_user_id, friend, approval) VALUES(3, 1, 1);
INSERT INTO friends(primary_user_id, friend, approval) VALUES(1, 4, 1);
INSERT INTO friends(primary_user_id, friend, approval) VALUES(4, 1, 1);

INSERT INTO tags(tag_name) VALUES("??????");
INSERT INTO tags(tag_name) VALUES("??????");
INSERT INTO tags(tag_name) VALUES("?????????");
INSERT INTO tags(tag_name) VALUES("????????????");

INSERT INTO user_tags(primary_user_id, tag_id) VALUES(2, 1);
INSERT INTO user_tags(primary_user_id, tag_id) VALUES(2, 3);
INSERT INTO user_tags(primary_user_id, tag_id) VALUES(3, 3);


-- INSERT INTO users(mail,name) VALUES("exemple@exemple2.com","user2");
-- INSERT INTO users(mail,name) VALUES("exemple@exemple3.com","user3");
-- INSERT INTO users(mail,name) VALUES("exemple@exemple4.com","user4");
-- INSERT INTO users(mail,name) VALUES("exemple@exemple5.com","user5");

