ALTER TABLE batch
      ADD plateName VARCHAR(50) NOT NULL
    , ADD halfPlate CHAR(1) NOT NULL
    , ADD humidity DECIMAL(6,2) NOT NULL
    , ADD primerBatch VARCHAR(50) NOT NULL
    , ADD enzymeBatch VARCHAR(50) NOT NULL
    , ADD rotorGene VARCHAR(50) NOT NULL
;

ALTER TABLE batch_audit
      ADD plateName VARCHAR(50) NOT NULL
    , ADD halfPlate CHAR(1) NOT NULL
    , ADD humidity DECIMAL(6,2) NOT NULL
    , ADD primerBatch VARCHAR(50) NOT NULL
    , ADD enzymeBatch VARCHAR(50) NOT NULL
    , ADD rotorGene VARCHAR(50) NOT NULL
;

DROP TRIGGER trg_batch_insert;
CREATE TRIGGER trg_batch_insert AFTER INSERT ON batch
    FOR EACH ROW
    BEGIN
        INSERT INTO batch_audit(audit_action, audit_datetime, batchId, batchCode, robot, pcrMachine, temperature, datetime, userId, version_id, plateName, halfPlate, humidity, primerBatch, enzymeBatch, rotorGene)
        VALUES ('INSERT NEW',NOW(),NEW.id, NEW.batchCode, NEW.robot, NEW.pcrMachine, NEW.temperature, NEW.datetime, NEW.userId, NEW.version_id, NEW.plateName, NEW.halfPlate, NEW.humidity, NEW.primerBatch, NEW.enzymeBatch, NEW.rotorGene);
    END
;

DROP TRIGGER trg_batch_update;
CREATE TRIGGER trg_batch_update AFTER UPDATE ON batch
    FOR EACH ROW
    BEGIN
        INSERT INTO batch_audit(audit_action, audit_datetime, batchId, batchCode, robot, pcrMachine, temperature, datetime, userId, version_id, plateName, halfPlate, humidity, primerBatch, enzymeBatch, rotorGene)
        VALUES ('UPDATE OLD',NOW(),OLD.id, OLD.batchCode, OLD.robot, OLD.pcrMachine, OLD.temperature, OLD.datetime, OLD.userId, OLD.version_id, OLD.plateName, OLD.halfPlate, OLD.humidity, OLD.primerBatch, OLD.enzymeBatch, OLD.rotorGene);
        INSERT INTO batch_audit(audit_action, audit_datetime, batchId, batchCode, robot, pcrMachine, temperature, datetime, userId, version_id, plateName, halfPlate, humidity, primerBatch, enzymeBatch, rotorGene)
        VALUES ('UPDATE NEW',NOW(),NEW.id, NEW.batchCode, NEW.robot, NEW.pcrMachine, NEW.temperature, NEW.datetime, NEW.userId, NEW.version_id, NEW.plateName, NEW.halfPlate, NEW.humidity, NEW.primerBatch, NEW.enzymeBatch, NEW.rotorGene);
    END
;

DROP TRIGGER trg_batch_delete;
CREATE TRIGGER trg_batch_delete AFTER DELETE ON batch
    FOR EACH ROW
    BEGIN
        INSERT INTO batch_audit(audit_action, audit_datetime, batchId, batchCode, robot, pcrMachine, temperature, datetime, userId, version_id, plateName, halfPlate, humidity, primerBatch, enzymeBatch, rotorGene)
        VALUES ('DELETE OLD',NOW(),OLD.id, OLD.batchCode, OLD.robot, OLD.pcrMachine, OLD.temperature, OLD.datetime, OLD.userId, OLD.version_id, OLD.plateName, OLD.halfPlate, OLD.humidity, OLD.primerBatch, OLD.enzymeBatch, OLD.rotorGene);
    END
;
