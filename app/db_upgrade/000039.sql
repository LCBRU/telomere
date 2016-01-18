DROP TRIGGER trg_samplePlate_update;

ALTER TABLE samplePlate
    ADD dnaTest_tmp DECIMAL(12,2),
    ADD picoTest_tmp DECIMAL(12,2)
;

ALTER TABLE samplePlate_audit
    ADD dnaTest_tmp DECIMAL(12,2),
    ADD picoTest_tmp DECIMAL(12,2)
;

UPDATE samplePlate
SET dnaTest_tmp = dnaTest,
    picoTest_tmp = picoTest
    ;

UPDATE samplePlate_audit
SET dnaTest_tmp = dnaTest,
    picoTest_tmp = picoTest
;

ALTER TABLE samplePlate
    DROP COLUMN dnaTest,
    DROP COLUMN picoTest
;

ALTER TABLE samplePlate_audit
    DROP COLUMN dnaTest,
    DROP COLUMN picoTest
;

ALTER TABLE samplePlate
    ADD dnaTest DECIMAL(12,2) NULL,
    ADD picoTest DECIMAL(12,2) NULL
;

ALTER TABLE samplePlate_audit
    ADD dnaTest DECIMAL(12,2) NULL,
    ADD picoTest DECIMAL(12,2) NULL
;

UPDATE samplePlate
SET dnaTest = dnaTest_tmp,
    picoTest = picoTest_tmp
 ;

UPDATE samplePlate_audit
SET dnaTest = dnaTest_tmp,
    picoTest = picoTest_tmp
;

ALTER TABLE samplePlate
    DROP COLUMN dnaTest_tmp,
    DROP COLUMN picoTest_tmp
;

ALTER TABLE samplePlate_audit
    DROP COLUMN dnaTest_tmp,
    DROP COLUMN picoTest_tmp
;

CREATE TRIGGER trg_samplePlate_update AFTER UPDATE ON samplePlate
    FOR EACH ROW
    BEGIN
		INSERT INTO samplePlate_audit(audit_action, audit_datetime, samplePlateId, sampleCode, manifestId, plateName, well, volume, conditionDescription, dnaTest, picoTest)
		VALUES ('UPDATE OLD', NOW(), OLD.id, OLD.sampleCode, OLD.manifestId, OLD.plateName, OLD.well, OLD.volume, OLD.conditionDescription, OLD.dnaTest, OLD.picoTest);
		INSERT INTO samplePlate_audit(audit_action, audit_datetime, samplePlateId, sampleCode, manifestId, plateName, well, volume, conditionDescription, dnaTest, picoTest)
		VALUES ('UPDATE NEW', NOW(), NEW.id, NEW.sampleCode, NEW.manifestId, NEW.plateName, NEW.well, NEW.volume, NEW.conditionDescription, NEW.dnaTest, NEW.picoTest);
    END
;

