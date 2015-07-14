CREATE TABLE measurement (
        id INTEGER PRIMARY KEY AUTO_INCREMENT
    ,   batchId INTEGER NOT NULL
    ,   sampleId INTEGER NOT NULL
    ,	t1 DECIMAL(5,2) NOT NULL
    ,	s1 DECIMAL(5,2) NOT NULL
    ,	t2 DECIMAL(5,2) NOT NULL
    ,	s2 DECIMAL(5,2) NOT NULL
    ,	tsRatio DECIMAL(5,2) NOT NULL
	,	CONSTRAINT fk_measurement_batch FOREIGN KEY (batchId) REFERENCES batch(Id)
	,	CONSTRAINT fk_measurement_sample FOREIGN KEY (sampleId) REFERENCES sample(Id)
    )
;

CREATE INDEX idx_sample_batchId
ON sample (batchId)
;

CREATE INDEX idx_sample_sampleId
ON sample (sampleId)
;
