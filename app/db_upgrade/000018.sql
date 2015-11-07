ALTER TABLE sample
      DROP COLUMN concentration
    , DROP COLUMN plateId
    , DROP COLUMN volume
;

ALTER TABLE sample
      ADD plateName VARCHAR(50) NOT NULL
    , ADD well VARCHAR(50) NOT NULL
    , ADD conditionDescription VARCHAR(50) NOT NULL
    , ADD dnaTest DECIMAL(6,2) NOT NULL
    , ADD picoTest DECIMAL(6,2) NOT NULL
    , ADD volume DECIMAL(6,2) NOT NULL
;

ALTER TABLE sample_audit
      DROP COLUMN concentration
    , DROP COLUMN plateId
    , DROP COLUMN volume
;

ALTER TABLE sample_audit
      ADD plateName VARCHAR(50) NOT NULL
    , ADD well VARCHAR(50) NOT NULL
    , ADD conditionDescription VARCHAR(50) NOT NULL
    , ADD dnaTest DECIMAL(6,2) NOT NULL
    , ADD picoTest DECIMAL(6,2) NOT NULL
    , ADD volume DECIMAL(6,2) NOT NULL
;

DROP TRIGGER trg_sample_insert;
CREATE TRIGGER trg_sample_insert AFTER INSERT ON sample
    FOR EACH ROW
    BEGIN
		INSERT INTO sample_audit(audit_action, audit_datetime, sampleId, sampleCode, volume, plateName, well, conditionDescription, dnaTest, picoTest)
		VALUES ('INSERT NEW',NOW(),NEW.id, NEW.sampleCode, NEW.volume, NEW.plateName, NEW.well, NEW.conditionDescription, NEW.dnaTest, NEW.picoTest);
    END
;

DROP TRIGGER trg_sample_update;
CREATE TRIGGER trg_sample_update AFTER UPDATE ON sample
    FOR EACH ROW
    BEGIN
		INSERT INTO sample_audit(audit_action, audit_datetime, sampleId, sampleCode, volume, plateName, well, conditionDescription, dnaTest, picoTest)
		VALUES ('UPDATE OLD',NOW(),OLD.id, OLD.sampleCode, OLD.volume, OLD.plateName, OLD.well, OLD.conditionDescription, OLD.dnaTest, OLD.picoTest);
        INSERT INTO sample_audit(audit_action, audit_datetime, sampleId, sampleCode, volume, plateName, well, conditionDescription, dnaTest, picoTest)
        VALUES ('UPDATE NEW',NOW(),NEW.id, NEW.sampleCode, NEW.volume, NEW.plateName, NEW.well, NEW.conditionDescription, NEW.dnaTest, NEW.picoTest);
    END
;

DROP TRIGGER trg_sample_delete;
CREATE TRIGGER trg_sample_delete AFTER DELETE ON sample
    FOR EACH ROW
    BEGIN
        INSERT INTO sample_audit(audit_action, audit_datetime, sampleId, sampleCode, volume, plateName, well, conditionDescription, dnaTest, picoTest)
        VALUES ('DELETE OLD',NOW(),OLD.id, OLD.sampleCode, OLD.volume, OLD.plateName, OLD.well, OLD.conditionDescription, OLD.dnaTest, OLD.picoTest);
    END
;

