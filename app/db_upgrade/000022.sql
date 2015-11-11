CREATE TABLE completedError (
        id INTEGER PRIMARY KEY AUTO_INCREMENT
    ,   description VARCHAR(200) NOT NULL
    ,   batchId INTEGER NOT NULL
    ,   sampleId INTEGER NOT NULL
    ,   completedByUserId INTEGER NOT NULL
    ,   completedDatetime DATETIME NOT NULL
    ,   CONSTRAINT fk_completedError_batch FOREIGN KEY (batchId) REFERENCES batch(Id)
    ,   CONSTRAINT fk_completedError_sample FOREIGN KEY (sampleId) REFERENCES sample(Id)
    ,   CONSTRAINT fk_completedError_completedByUser FOREIGN KEY (completedByUserId) REFERENCES user(Id)
    )
;

CREATE INDEX idx_completedError_batchId
ON completedError (batchId)
;

CREATE INDEX idx_completedError_sampleId
ON completedError (sampleId)
;

CREATE INDEX idx_completedError_completedByUserId
ON completedError (completedByUserId)
;

CREATE TABLE completedError_audit
        audit_id INTEGER PRIMARY KEY AUTO_INCREMENT
    ,   audit_action VARCHAR(50) NOT NULL
    ,   audit_datetime DATETIME NOT NULL
    ,   completedErrorid INTEGER NOT NULL
    ,   description VARCHAR(200) NOT NULL
    ,   batchId INTEGER NOT NULL
    ,   sampleId INTEGER NOT NULL
    ,   completedByUserId INTEGER NOT NULL
    ,   completedDatetime DATETIME NOT NULL
;

CREATE TRIGGER trg_completedError_insert AFTER INSERT ON completedError
    FOR EACH ROW
    BEGIN
        INSERT INTO batch_audit(audit_action, audit_datetime, completedErrorId, description, batchId, sampleId, completedByUserId, completedDatetime)
        VALUES ('INSERT NEW',NOW(),NEW.id, NEW.description, NEW.batchId, NEW.sampleId, NEW.completedByUserId, NEW.completedDatetime);
    END
;

CREATE TRIGGER trg_completedError_update AFTER UPDATE ON completedError
    FOR EACH ROW
    BEGIN
        INSERT INTO batch_audit(audit_action, audit_datetime, completedErrorid, description, batchId, sampleId, completedByUserId, completedDatetime)
        VALUES ('UPDATE OLD',NOW(),OLD.id, OLD.description, OLD.batchId, OLD.sampleId, OLD.completedByUserId, OLD.completedDatetime);
        INSERT INTO batch_audit(audit_action, audit_datetime, completedErrorId, description, batchId, sampleId, completedByUserId, completedDatetime)
        VALUES ('UPDATE NEW',NOW(),NEW.id, NEW.description, NEW.batchId, NEW.sampleId, NEW.completedByUserId, NEW.completedDatetime);
    END
;

CREATE TRIGGER trg_completedError_delete AFTER DELETE ON completedError
    FOR EACH ROW
    BEGIN
        INSERT INTO batch_audit(audit_action, audit_datetime, completedErrorid, description, batchId, sampleId, completedByUserId, completedDatetime)
        VALUES ('DELETE OLD',NOW(),OLD.id, OLD.description, OLD.batchId, OLD.sampleId, OLD.completedByUserId, OLD.completedDatetime);
    END
;
