CREATE TABLE sample (
        id INTEGER PRIMARY KEY AUTO_INCREMENT
    ,   sampleCode VARCHAR(20) NOT NULL
    )
;

CREATE UNIQUE INDEX idx_sample_sampleCode
ON sample (sampleCode)
;
