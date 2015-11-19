ALTER TABLE batch
      DROP COLUMN batchCode
;

ALTER TABLE batch_audit
      DROP COLUMN batchCode
;

DROP TRIGGER trg_batch_insert;
CREATE TRIGGER trg_batch_insert AFTER INSERT ON batch
    FOR EACH ROW
    BEGIN
        INSERT INTO batch_audit(audit_action, audit_datetime, batchId, robot, pcrMachine, temperature, datetime, userId, version_id, plateName, halfPlate, humidity, primerBatch, enzymeBatch, rotorGene, operatorUserId)
        VALUES ('INSERT NEW',NOW(),NEW.id, NEW.robot, NEW.pcrMachine, NEW.temperature, NEW.datetime, NEW.userId, NEW.version_id, NEW.plateName, NEW.halfPlate, NEW.humidity, NEW.primerBatch, NEW.enzymeBatch, NEW.rotorGene, NEW.operatorUserId);
    END
;

DROP TRIGGER trg_batch_update;
CREATE TRIGGER trg_batch_update AFTER UPDATE ON batch
    FOR EACH ROW
    BEGIN
        INSERT INTO batch_audit(audit_action, audit_datetime, batchId, robot, pcrMachine, temperature, datetime, userId, version_id, plateName, halfPlate, humidity, primerBatch, enzymeBatch, rotorGene, operatorUserId)
        VALUES ('UPDATE OLD',NOW(),OLD.id, OLD.robot, OLD.pcrMachine, OLD.temperature, OLD.datetime, OLD.userId, OLD.version_id, OLD.plateName, OLD.halfPlate, OLD.humidity, OLD.primerBatch, OLD.enzymeBatch, OLD.rotorGene, OLD.operatorUserId);
        INSERT INTO batch_audit(audit_action, audit_datetime, batchId, robot, pcrMachine, temperature, datetime, userId, version_id, plateName, halfPlate, humidity, primerBatch, enzymeBatch, rotorGene, operatorUserId)
        VALUES ('UPDATE NEW',NOW(),NEW.id, NEW.robot, NEW.pcrMachine, NEW.temperature, NEW.datetime, NEW.userId, NEW.version_id, NEW.plateName, NEW.halfPlate, NEW.humidity, NEW.primerBatch, NEW.enzymeBatch, NEW.rotorGene, NEW.operatorUserId);
    END
;

DROP TRIGGER trg_batch_delete;
CREATE TRIGGER trg_batch_delete AFTER DELETE ON batch
    FOR EACH ROW
    BEGIN
        INSERT INTO batch_audit(audit_action, audit_datetime, batchId, robot, pcrMachine, temperature, datetime, userId, version_id, plateName, halfPlate, humidity, primerBatch, enzymeBatch, rotorGene, operatorUserId)
        VALUES ('DELETE OLD',NOW(),OLD.id, OLD.robot, OLD.pcrMachine, OLD.temperature, OLD.datetime, OLD.userId, OLD.version_id, OLD.plateName, OLD.halfPlate, OLD.humidity, OLD.primerBatch, OLD.enzymeBatch, OLD.rotorGene, OLD.operatorUserId);
    END
;
