CREATE TABLE manifest (
        id INTEGER PRIMARY KEY AUTO_INCREMENT
    ,   filename VARCHAR(500) NOT NULL
    ,   uploaded DATETIME NOT NULL
    ,   userId INTEGER NOT NULL
    ,   CONSTRAINT fk_manifest_user FOREIGN KEY (userId) REFERENCES user(Id)
    )
;

CREATE INDEX idx_manifest_userId
ON manifest (userId)
;
