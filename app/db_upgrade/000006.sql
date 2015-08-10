CREATE TABLE spreadsheet (
        id INTEGER PRIMARY KEY AUTO_INCREMENT
    ,   filename VARCHAR(500) NOT NULL
    ,   uploaded DATETIME NOT NULL
    ,   userId INTEGER NOT NULL
    ,   CONSTRAINT fk_spreadsheet_user FOREIGN KEY (userId) REFERENCES user(Id)
    )
;

CREATE INDEX idx_spreadsheet_userId
ON spreadsheet (userId)
;
