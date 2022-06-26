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
	delete_flg BOOLEAN DEFAULT 0
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

CREATE TABLE follows(
	follow_id INT(12) PRIMARY KEY AUTO_INCREMENT,
	follow_user INT(9),
	follower_user INT(9),
	created_at  DATETIME default current_timestamp,
	updated_at  DATETIME default current_timestamp on update current_timestamp,
	delete_flg BOOLEAN DEFAULT 0,
	FOREIGN KEY(follow_user)
	REFERENCES users(primary_user_id),
	FOREIGN KEY(follower_user)
	REFERENCES users(primary_user_id)
);

CREATE TABLE pull_notifications(
    pull_notification_id INT(12) PRIMARY KEY AUTO_INCREMENT,
    notification_type INT(1),
    notification_text VARCHAR(256),
    primary_user_id INT(9),
    partner_user_id INT(9),
    in_read BOOLEAN DEFAULT 0,
    created_at  DATETIME default current_timestamp,
    updated_at  DATETIME default current_timestamp on update current_timestamp,
    delete_flg BOOLEAN DEFAULT 0,
    FOREIGN KEY(primary_user_id)
    REFERENCES users(primary_user_id),
    FOREIGN KEY(partner_user_id)
    REFERENCES users(primary_user_id)
);





INSERT INTO users(user_id,user_name,user_image_pass,bio) VALUES("Shishamo_Love","ししゃも","./","こんばんは！暇なときはゲームしています！気軽に誘ってね♡");
INSERT INTO users(user_id,user_name,user_image_pass,bio) VALUES("BGY32ff9weg","しゃけ","./","ご飯食べに行こー！！");
INSERT INTO users(user_id,user_name,user_image_pass,bio) VALUES("sawara_0325","さわら","./","寿司しか勝たん💪");
INSERT INTO users(user_id,user_name,user_image_pass,bio) VALUES("tuna532","まぐろ","./","7/2日遊べる人募集中");
INSERT INTO users(user_id,user_name,user_image_pass,bio) VALUES("taidayo_","たい","./","今月忙しいかも💦");
INSERT INTO users(user_id,user_name,user_image_pass,bio) VALUES("like_fugu_lile","ふぐ","./","20↑アニメが好きです");
INSERT INTO users(user_id,user_name,user_image_pass,bio) VALUES("gcwu9e0hfeu","かに","./","焼肉食べたい🤤");
INSERT INTO users(user_id,user_name,user_image_pass,bio) VALUES("ebi_0019","えび","./","🍤");
INSERT INTO users(user_id,user_name,user_image_pass,bio) VALUES("ji0h3fhjweuh02","たちうお","./","仕事中~");
INSERT INTO users(user_id,user_name,user_image_pass,bio) VALUES("8_oct","たこ","./","フィンランド🇫🇮なう！");


-- INSERT INTO users(mail,name) VALUES("exemple@exemple2.com","user2");
-- INSERT INTO users(mail,name) VALUES("exemple@exemple3.com","user3");
-- INSERT INTO users(mail,name) VALUES("exemple@exemple4.com","user4");
-- INSERT INTO users(mail,name) VALUES("exemple@exemple5.com","user5");

