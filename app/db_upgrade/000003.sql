CREATE TABLE batch (
        id INTEGER PRIMARY KEY AUTO_INCREMENT
    ,   batchCode VARCHAR(20) NOT NULL
    ,	robot VARCHAR(20) NOT NULL
    ,	pcrMachine VARCHAR(20) NOT NULL
    ,	temperature DECIMAL(3,1) NOT NULL
    ,	datetime DATETIME NOT NULL
    ,	userId INTEGER NOT NULL
	,	CONSTRAINT fk_batch_user FOREIGN KEY (userId) REFERENCES user(Id)
    )
;

CREATE INDEX idx_batch_userId
ON batch (userId)
;

CREATE UNIQUE INDEX idx_batch_batchCode
ON batch (batchCode)
;
