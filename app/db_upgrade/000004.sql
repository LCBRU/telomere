CREATE TABLE sample (
        id INTEGER PRIMARY KEY AUTO_INCREMENT
    ,   sampleId VARCHAR(20) NOT NULL
    )
;

CREATE UNIQUE INDEX idx_sample_sampleId
ON sample (sampleId)
;
