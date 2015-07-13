CREATE TABLE user (
        id INTEGER PRIMARY KEY AUTO_INCREMENT
    ,   username VARCHAR(50) NOT NULL
    ,	CONSTRAINT uc_username UNIQUE (username)
    )


