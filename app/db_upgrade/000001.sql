CREATE TABLE user (
        id INTEGER PRIMARY KEY AUTO_INCREMENT
    ,   username VARCHAR(50) NOT NULL
    )
;

CREATE UNIQUE INDEX idx_user_username
ON user (username)
;
