# Batch
CREATE TABLE batch_audit (
        audit_id INTEGER PRIMARY KEY AUTO_INCREMENT
    ,   audit_action VARCHAR(50) NOT NULL
    ,   audit_datetime DATETIME NOT NULL
    ,   batchId INTEGER NOT NULL
    ,   batchCode VARCHAR(20) NOT NULL
    ,	robot VARCHAR(20) NOT NULL
    ,	pcrMachine VARCHAR(20) NOT NULL
    ,	temperature DECIMAL(3,1) NOT NULL
    ,	datetime DATETIME NOT NULL
    ,	userId INTEGER NOT NULL
    ,	version_id INTEGER NOT NULL
    )
;

CREATE TRIGGER trg_batch_insert AFTER INSERT ON batch
    FOR EACH ROW
    BEGIN
		INSERT INTO batch_audit(audit_action, audit_datetime, batchId, batchCode, robot, pcrMachine, temperature, datetime, userId, version_id)
		VALUES ('INSERT NEW',NOW(),NEW.id, NEW.batchCode, NEW.robot, NEW.pcrMachine, NEW.temperature, NEW.datetime, NEW.userId, NEW.version_id);
    END
;

CREATE TRIGGER trg_batch_update AFTER UPDATE ON batch
    FOR EACH ROW
    BEGIN
		INSERT INTO batch_audit(audit_action, audit_datetime, batchId, batchCode, robot, pcrMachine, temperature, datetime, userId, version_id)
		VALUES ('UPDATE OLD',NOW(),OLD.id, OLD.batchCode, OLD.robot, OLD.pcrMachine, OLD.temperature, OLD.datetime, OLD.userId, OLD.version_id);
		INSERT INTO batch_audit(audit_action, audit_datetime, batchId, batchCode, robot, pcrMachine, temperature, datetime, userId, version_id)
		VALUES ('UPDATE NEW',NOW(),NEW.id, NEW.batchCode, NEW.robot, NEW.pcrMachine, NEW.temperature, NEW.datetime, NEW.userId, NEW.version_id);
    END
;

CREATE TRIGGER trg_batch_delete AFTER DELETE ON batch
    FOR EACH ROW
    BEGIN
		INSERT INTO batch_audit(audit_action, audit_datetime, batchId, batchCode, robot, pcrMachine, temperature, datetime, userId, version_id)
		VALUES ('DELETE OLD',NOW(),OLD.id, OLD.batchCode, OLD.robot, OLD.pcrMachine, OLD.temperature, OLD.datetime, OLD.userId, OLD.version_id);
    END
;

# Sample
CREATE TABLE sample_audit (
        audit_id INTEGER PRIMARY KEY AUTO_INCREMENT
    ,   audit_action VARCHAR(50) NOT NULL
    ,   audit_datetime DATETIME NOT NULL
    ,   sampleId INTEGER NOT NULL
    ,   sampleCode VARCHAR(20) NOT NULL
    )
;

CREATE TRIGGER trg_sample_insert AFTER INSERT ON sample
    FOR EACH ROW
    BEGIN
		INSERT INTO sample_audit(audit_action, audit_datetime, sampleId, sampleCode)
		VALUES ('INSERT NEW',NOW(),NEW.id, NEW.sampleCode);
    END
;

CREATE TRIGGER trg_sample_update AFTER UPDATE ON sample
    FOR EACH ROW
    BEGIN
		INSERT INTO sample_audit(audit_action, audit_datetime, sampleId, sampleCode)
		VALUES ('UPDATE OLD',NOW(),OLD.id, OLD.sampleCode);
		INSERT INTO sample_audit(audit_action, audit_datetime, sampleId, sampleCode)
		VALUES ('UPDATE NEW',NOW(),NEW.id, NEW.sampleCode);
    END
;

CREATE TRIGGER trg_sample_delete AFTER DELETE ON sample
    FOR EACH ROW
    BEGIN
		INSERT INTO sample_audit(audit_action, audit_datetime, sampleId, sampleCode)
		VALUES ('DELETE OLD',NOW(),OLD.id, OLD.sampleCode);
    END
;

# Measurement
CREATE TABLE measurement_audit (
        audit_id INTEGER PRIMARY KEY AUTO_INCREMENT
    ,   audit_action VARCHAR(50) NOT NULL
    ,   audit_datetime DATETIME NOT NULL
    ,   measurementId INTEGER NOT NULL
    ,   batchId INTEGER NOT NULL
    ,   sampleId INTEGER NOT NULL
    ,	t1 DECIMAL(5,2) NOT NULL
    ,	s1 DECIMAL(5,2) NOT NULL
    ,	t2 DECIMAL(5,2) NOT NULL
    ,	s2 DECIMAL(5,2) NOT NULL
    )
;

CREATE TRIGGER trg_measurement_insert AFTER INSERT ON measurement
    FOR EACH ROW
    BEGIN
		INSERT INTO measurement_audit(audit_action, audit_datetime, measurementId, batchId, sampleId, t1, s1, t2, s2)
		VALUES ('INSERT NEW',NOW(),NEW.id, NEW.batchId, NEW.sampleId, NEW.t1, NEW.s1, NEW.t2, NEW.s2);
    END
;

CREATE TRIGGER trg_measurement_update AFTER UPDATE ON measurement
    FOR EACH ROW
    BEGIN
		INSERT INTO measurement_audit(audit_action, audit_datetime, measurementId, batchId, sampleId, t1, s1, t2, s2)
		VALUES ('UPDATE OLD',NOW(),OLD.id, OLD.batchId, OLD.sampleId, OLD.t1, OLD.s1, OLD.t2, OLD.s2);
		INSERT INTO measurement_audit(audit_action, audit_datetime, measurementId, batchId, sampleId, t1, s1, t2, s2)
		VALUES ('UPDATE NEW',NOW(),NEW.id, NEW.batchId, NEW.sampleId, NEW.t1, NEW.s1, NEW.t2, NEW.s2);
    END
;

CREATE TRIGGER trg_measurement_delete AFTER DELETE ON measurement
    FOR EACH ROW
    BEGIN
		INSERT INTO measurement_audit(audit_action, audit_datetime, measurementId, batchId, sampleId, t1, s1, t2, s2)
		VALUES ('DELETE OLD',NOW(),OLD.id, OLD.batchId, OLD.sampleId, OLD.t1, OLD.s1, OLD.t2, OLD.s2);
    END
;

# Spreadsheet
CREATE TABLE spreadsheet_audit (
        id INTEGER PRIMARY KEY AUTO_INCREMENT
    ,   audit_action VARCHAR(50) NOT NULL
    ,   audit_datetime DATETIME NOT NULL
    ,   spreadsheetId INTEGER NOT NULL
    ,   filename VARCHAR(500) NOT NULL
    ,   uploaded DATETIME NOT NULL
    ,   userId INTEGER NOT NULL
    ,   batchId INTEGER NOT NULL
    )
;

CREATE TRIGGER trg_spreadsheet_insert AFTER INSERT ON spreadsheet
    FOR EACH ROW
    BEGIN
		INSERT INTO spreadsheet_audit(audit_action, audit_datetime, spreadsheetId, filename, uploaded, userId, batchId)
		VALUES ('INSERT NEW',NOW(),NEW.id, NEW.filename, NEW.uploaded, NEW.userId, NEW.batchId);
    END
;

CREATE TRIGGER trg_spreadsheet_update AFTER UPDATE ON spreadsheet
    FOR EACH ROW
    BEGIN
		INSERT INTO spreadsheet_audit(audit_action, audit_datetime, spreadsheetId, filename, uploaded, userId, batchId)
		VALUES ('UPDATE OLD',NOW(),OLD.id, OLD.filename, OLD.uploaded, OLD.userId, OLD.batchId);
		INSERT INTO spreadsheet_audit(audit_action, audit_datetime, spreadsheetId, filename, uploaded, userId, batchId)
		VALUES ('UPDATE NEW',NOW(),NEW.id, NEW.filename, NEW.uploaded, NEW.userId, NEW.batchId);
    END
;

CREATE TRIGGER trg_spreadsheet_delete AFTER DELETE ON spreadsheet
    FOR EACH ROW
    BEGIN
		INSERT INTO spreadsheet_audit(audit_action, audit_datetime, spreadsheetId, filename, uploaded, userId, batchId)
		VALUES ('DELETE OLD',NOW(),OLD.id, OLD.filename, OLD.uploaded, OLD.userId, OLD.batchId);
    END
;

