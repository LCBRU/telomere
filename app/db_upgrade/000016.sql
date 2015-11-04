CREATE TABLE manifest_audit (
        id INTEGER PRIMARY KEY AUTO_INCREMENT
    ,   audit_action VARCHAR(50) NOT NULL
    ,   audit_datetime DATETIME NOT NULL
    ,   manifestId INTEGER NOT NULL
    ,   filename VARCHAR(500) NOT NULL
    ,   uploaded DATETIME NOT NULL
    ,   userId INTEGER NOT NULL
    ,   batchId INTEGER NOT NULL
    )
;

CREATE TRIGGER trg_manifest_insert AFTER INSERT ON manifest
    FOR EACH ROW
    BEGIN
		INSERT INTO manifest_audit(audit_action, audit_datetime, manifestId, filename, uploaded, userId, batchId)
		VALUES ('INSERT NEW',NOW(),NEW.id, NEW.filename, NEW.uploaded, NEW.userId, NEW.batchId);
    END
;

CREATE TRIGGER trg_manifest_update AFTER UPDATE ON manifest
    FOR EACH ROW
    BEGIN
		INSERT INTO manifest_audit(audit_action, audit_datetime, manifestId, filename, uploaded, userId, batchId)
		VALUES ('UPDATE OLD',NOW(),OLD.id, OLD.filename, OLD.uploaded, OLD.userId, OLD.batchId);
		INSERT INTO manifest_audit(audit_action, audit_datetime, manifestId, filename, uploaded, userId, batchId)
		VALUES ('UPDATE NEW',NOW(),NEW.id, NEW.filename, NEW.uploaded, NEW.userId, NEW.batchId);
    END
;

CREATE TRIGGER trg_manifest_delete AFTER DELETE ON manifest
    FOR EACH ROW
    BEGIN
		INSERT INTO manifest_audit(audit_action, audit_datetime, manifestId, filename, uploaded, userId, batchId)
		VALUES ('DELETE OLD',NOW(),OLD.id, OLD.filename, OLD.uploaded, OLD.userId, OLD.batchId);
    END
;

