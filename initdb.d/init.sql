USE sample_db;

CREATE TABLE users(
	user_id INT(8) PRIMARY KEY AUTO_INCREMENT,
	mail VARCHAR(128) NOT NULL UNIQUE,
	name VARCHAR(64) NOT NULL);

INSERT INTO users(mail,name) VALUES("exemple@exemple1.com","user1");
INSERT INTO users(mail,name) VALUES("exemple@exemple2.com","user2");
INSERT INTO users(mail,name) VALUES("exemple@exemple3.com","user3");
INSERT INTO users(mail,name) VALUES("exemple@exemple4.com","user4");
INSERT INTO users(mail,name) VALUES("exemple@exemple5.com","user5");

