CREATE TABLE user (
        id INTEGER PRIMARY KEY AUTO_INCREMENT
    ,   username VARCHAR(50) NOT NULL
    ,   code VARCHAR(10) NOT NULL
    )
;

CREATE UNIQUE INDEX idx_user_username
ON user (username)
;

CREATE UNIQUE INDEX idx_user_code
ON user (code)
;
