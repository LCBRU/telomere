CREATE TABLE batch (
        id INTEGER PRIMARY KEY AUTO_INCREMENT
    ,   batchId VARCHAR(20) NOT NULL
    ,	robot VARCHAR(20) NOT NULL
    ,	pcrMachine VARCHAR(20) NOT NULL
    ,	temperature DECIMAL(3,1) NOT NULL
    ,	datetime DATETIME NOT NULL
    )


