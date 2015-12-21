ALTER TABLE sample
	DROP COLUMN plateName,
	DROP COLUMN well,
	DROP COLUMN conditionDescription,
	DROP COLUMN dnaTest,
	DROP COLUMN picoTest,
	DROP COLUMN manifestId,
	DROP COLUMN volume,
	DROP FOREIGN KEY fk_sample_manifest,
	DROP INDEX idx_sample_manifestId
;

ALTER TABLE sample_audit
	DROP COLUMN plateName,
	DROP COLUMN well,
	DROP COLUMN conditionDescription,
	DROP COLUMN dnaTest,
	DROP COLUMN picoTest,
	DROP COLUMN manifestId,
	DROP COLUMN volume
;

DROP TRIGGER trg_sample_insert;
CREATE TRIGGER trg_sample_insert AFTER INSERT ON sample
    FOR EACH ROW
    BEGIN
		INSERT INTO sample_audit(audit_action, audit_datetime, sampleId, sampleCode)
		VALUES ('INSERT NEW',NOW(),NEW.id, NEW.sampleCode);
    END
;

DROP TRIGGER trg_sample_update;
CREATE TRIGGER trg_sample_update AFTER UPDATE ON sample
    FOR EACH ROW
    BEGIN
		INSERT INTO sample_audit(audit_action, audit_datetime, sampleId, sampleCode)
		VALUES ('UPDATE OLD',NOW(),OLD.id, OLD.sampleCode);
        INSERT INTO sample_audit(audit_action, audit_datetime, sampleId, sampleCode)
        VALUES ('UPDATE NEW',NOW(),NEW.id, NEW.sampleCode);
    END
;

DROP TRIGGER trg_sample_delete;
CREATE TRIGGER trg_sample_delete AFTER DELETE ON sample
    FOR EACH ROW
    BEGIN
        INSERT INTO sample_audit(audit_action, audit_datetime, sampleId, sampleCode)
        VALUES ('DELETE OLD',NOW(),OLD.id, OLD.sampleCode);
    END
;

