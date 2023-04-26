CREATE TABLE users(
    user_id     INT(10) NOT NULL AUTO_INCREMENT,
    user_name   VARCHAR(30) NOT NULL,
    user_pass   VARCHAR(255) NOT NULL,
    UNIQUE INDEX user_name_unique (user_name),
    PRIMARY KEY (user_id)
);

CREATE TABLE topics(
    topic_id    INT(10) NOT NULL AUTO_INCREMENT,
    topic_name  VARCHAR(255) NOT NULL,
    UNIQUE INDEX topic_name_unique (topic_name),
    PRIMARY KEY (topic_id)
);

CREATE TABLE posts(
    post_id         INT(10) NOT NULL AUTO_INCREMENT,
    post_subject    VARCHAR(255) NOT NULL,
    post_date		DATETIME NOT NULL,
    post_topic      INT(10) NOT NULL,
    post_by         INT(10) NOT NULL,
    PRIMARY KEY (post_id)
);

CREATE TABLE reply(
    reply_id 		INT(10) NOT NULL AUTO_INCREMENT,
    reply_content	TEXT NOT NULL,
    reply_date 		DATETIME NOT NULL,
    reply_post		INT(10) NOT NULL,
    reply_by		INT(10) NOT NULL,
    PRIMARY KEY (reply_id)
);

ALTER TABLE posts ADD FOREIGN KEY(post_topic) REFERENCES topics(topic_id) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE posts ADD FOREIGN KEY(post_by) REFERENCES users(user_id) ON DELETE RESTRICT ON UPDATE CASCADE;

ALTER TABLE reply ADD FOREIGN KEY(reply_post) REFERENCES posts(post_id) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE reply ADD FOREIGN KEY(reply_by) REFERENCES users(user_id) ON DELETE RESTRICT ON UPDATE CASCADE;