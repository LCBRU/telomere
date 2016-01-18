CREATE TABLE samplePlate (
        id INTEGER PRIMARY KEY AUTO_INCREMENT
    ,   sampleCode VARCHAR(20)
    ,   manifestId INTEGER
    ,   plateName VARCHAR(50) NOT NULL
    ,	well VARCHAR(50) NOT NULL
    ,	volume INTEGER
    ,	conditionDescription VARCHAR(50) NOT NULL
    ,	dnaTest DECIMAL(12,2) NOT NULL
    ,   picoTest DECIMAL(12,2) NOT NULL
	,	CONSTRAINT fk_samplePlate_sampleCode FOREIGN KEY (sampleCode) REFERENCES sample(sampleCode)
	,	CONSTRAINT fk_samplePlate_manifest FOREIGN KEY (manifestId) REFERENCES manifest(Id)
)
;

CREATE INDEX idx_samplePlate_sampleCode
ON samplePlate (sampleCode)
;

CREATE UNIQUE INDEX idx_samplePlate_sampleCode_plateName
ON samplePlate (sampleCode, plateName)
;

CREATE INDEX idx_samplePlate_manifestId
ON samplePlate (manifestId)
;

CREATE TABLE samplePlate_audit (
        id INTEGER PRIMARY KEY AUTO_INCREMENT
    ,   audit_action VARCHAR(50) NOT NULL
    ,   audit_datetime DATETIME NOT NULL
    ,   samplePlateId INTEGER
    ,   sampleCode VARCHAR(20)
    ,   manifestId INTEGER
    ,   plateName VARCHAR(50) NOT NULL
    ,	well VARCHAR(50) NOT NULL
    ,	volume INTEGER
    ,	conditionDescription VARCHAR(50) NOT NULL
    ,	dnaTest DECIMAL(12,2) NOT NULL
    ,   picoTest DECIMAL(12,2) NOT NULL
)
;

CREATE TRIGGER trg_samplePlate_insert AFTER INSERT ON samplePlate
    FOR EACH ROW
    BEGIN
		INSERT INTO samplePlate_audit(audit_action, audit_datetime, samplePlateId, sampleCode, manifestId, plateName, well, volume, conditionDescription, dnaTest, picoTest)
		VALUES ('INSERT NEW', NOW(), NEW.id, NEW.sampleCode, NEW.manifestId, NEW.plateName, NEW.well, NEW.volume, NEW.conditionDescription, NEW.dnaTest, NEW.picoTest);
    END
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

CREATE TRIGGER trg_samplePlate_delete AFTER DELETE ON samplePlate
    FOR EACH ROW
    BEGIN
		INSERT INTO samplePlate_audit(audit_action, audit_datetime, samplePlateId, sampleCode, manifestId, plateName, well, volume, conditionDescription, dnaTest, picoTest)
		VALUES ('DELETE OLD', NOW(), OLD.id, OLD.sampleCode, OLD.manifestId, OLD.plateName, OLD.well, OLD.volume, OLD.conditionDescription, OLD.dnaTest, OLD.picoTest);
    END
;

