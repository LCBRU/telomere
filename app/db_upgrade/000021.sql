CREATE TABLE outstandingError (
        id INTEGER PRIMARY KEY AUTO_INCREMENT
    ,   description VARCHAR(200) NOT NULL
    ,   batchId INTEGER NOT NULL
    ,   sampleId INTEGER NOT NULL
    ,   CONSTRAINT fk_outstandingError_batch FOREIGN KEY (batchId) REFERENCES batch(Id)
    ,   CONSTRAINT fk_outstandingError_sample FOREIGN KEY (sampleId) REFERENCES sample(Id)
    )
;

CREATE INDEX idx_outstandingError_batchId
ON outstandingError (batchId)
;

CREATE INDEX idx_outstandingError_sampleId
ON outstandingError (sampleId)
;

CREATE TABLE outstandingError_audit (
        audit_id INTEGER PRIMARY KEY AUTO_INCREMENT
    ,   audit_action VARCHAR(50) NOT NULL
    ,   audit_datetime DATETIME NOT NULL
    ,   outstandingErrorid INTEGER NOT NULL
    ,   description VARCHAR(200) NOT NULL
    ,   batchId INTEGER NOT NULL
    ,   sampleId INTEGER NOT NULL
    )
;

CREATE TRIGGER trg_outstandingError_insert AFTER INSERT ON outstandingError
    FOR EACH ROW
    BEGIN
        INSERT INTO batch_audit(audit_action, audit_datetime, outstandingErrorId, description, batchId, sampleId)
        VALUES ('INSERT NEW',NOW(),NEW.id, NEW.description, NEW.batchId, NEW.sampleId);
    END
;

CREATE TRIGGER trg_outstandingError_update AFTER UPDATE ON outstandingError
    FOR EACH ROW
    BEGIN
        INSERT INTO batch_audit(audit_action, audit_datetime, outstandingErrorid, description, batchId, sampleId)
        VALUES ('UPDATE OLD',NOW(),OLD.id, OLD.description, OLD.batchId, OLD.sampleId);
        INSERT INTO batch_audit(audit_action, audit_datetime, outstandingErrorId, description, batchId, sampleId)
        VALUES ('UPDATE NEW',NOW(),NEW.id, NEW.description, NEW.batchId, NEW.sampleId);
    END
;

CREATE TRIGGER trg_outstandingError_delete AFTER DELETE ON outstandingError
    FOR EACH ROW
    BEGIN
        INSERT INTO batch_audit(audit_action, audit_datetime, outstandingErrorid, description, batchId, sampleId)
        VALUES ('DELETE OLD',NOW(),OLD.id, OLD.description, OLD.batchId, OLD.sampleId);
    END
;
