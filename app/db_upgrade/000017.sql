ALTER TABLE sample
      ADD volume DECIMAL(3,1) NOT NULL
    , ADD concentration DECIMAL(3,1) NOT NULL
    , ADD plateId VARCHAR(20) NOT NULL
;

ALTER TABLE sample_audit
      ADD volume DECIMAL(3,1) NOT NULL
    , ADD concentration DECIMAL(3,1) NOT NULL
    , ADD plateId VARCHAR(20) NOT NULL
;

DROP TRIGGER trg_sample_insert;
CREATE TRIGGER trg_sample_insert AFTER INSERT ON sample
    FOR EACH ROW
    BEGIN
		INSERT INTO sample_audit(audit_action, audit_datetime, sampleId, sampleCode, volume, concentration, plateId)
		VALUES ('INSERT NEW',NOW(),NEW.id, NEW.sampleCode, NEW.volume, NEW.concentration, NEW.plateId);
    END
;

DROP TRIGGER trg_sample_update;
CREATE TRIGGER trg_sample_update AFTER UPDATE ON sample
    FOR EACH ROW
    BEGIN
		INSERT INTO sample_audit(audit_action, audit_datetime, sampleId, sampleCode, volume, concentration, plateId)
		VALUES ('UPDATE OLD',NOW(),OLD.id, OLD.sampleCode, OLD.volume, OLD.concentration, OLD.plateId);
		INSERT INTO sample_audit(audit_action, audit_datetime, sampleId, sampleCode, volume, concentration, plateId)
		VALUES ('UPDATE NEW',NOW(),NEW.id, NEW.sampleCode, NEW.volume, NEW.concentration, NEW.plateId);
    END
;

DROP TRIGGER trg_sample_delete;
CREATE TRIGGER trg_sample_delete AFTER DELETE ON sample
    FOR EACH ROW
    BEGIN
		INSERT INTO sample_audit(audit_action, audit_datetime, sampleId, sampleCode, volume, concentration, plateId)
		VALUES ('DELETE OLD',NOW(),OLD.id, OLD.sampleCode, OLD.volume, OLD.concentration, OLD.plateId);
    END
;

