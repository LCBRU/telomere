ALTER TABLE batch
      ADD operatorUserId INTEGER NOT NULL
    , ADD CONSTRAINT fk_batch_operator FOREIGN KEY (operatorUserId) REFERENCES user(Id)
;

ALTER TABLE batch_audit
      ADD operatorUserId INTEGER NOT NULL
;

DROP TRIGGER trg_batch_insert;
CREATE TRIGGER trg_batch_insert AFTER INSERT ON batch
    FOR EACH ROW
    BEGIN
        INSERT INTO batch_audit(audit_action, audit_datetime, batchId, batchCode, robot, pcrMachine, temperature, datetime, userId, version_id, plateName, halfPlate, humidity, primerBatch, enzymeBatch, rotorGene, operatorUserId)
        VALUES ('INSERT NEW',NOW(),NEW.id, NEW.batchCode, NEW.robot, NEW.pcrMachine, NEW.temperature, NEW.datetime, NEW.userId, NEW.version_id, NEW.plateName, NEW.halfPlate, NEW.humidity, NEW.primerBatch, NEW.enzymeBatch, NEW.rotorGene, NEW.operatorUserId);
    END
;

DROP TRIGGER trg_batch_update;
CREATE TRIGGER trg_batch_update AFTER UPDATE ON batch
    FOR EACH ROW
    BEGIN
        INSERT INTO batch_audit(audit_action, audit_datetime, batchId, batchCode, robot, pcrMachine, temperature, datetime, userId, version_id, plateName, halfPlate, humidity, primerBatch, enzymeBatch, rotorGene, operatorUserId)
        VALUES ('UPDATE OLD',NOW(),OLD.id, OLD.batchCode, OLD.robot, OLD.pcrMachine, OLD.temperature, OLD.datetime, OLD.userId, OLD.version_id, OLD.plateName, OLD.halfPlate, OLD.humidity, OLD.primerBatch, OLD.enzymeBatch, OLD.rotorGene, OLD.operatorUserId);
        INSERT INTO batch_audit(audit_action, audit_datetime, batchId, batchCode, robot, pcrMachine, temperature, datetime, userId, version_id, plateName, halfPlate, humidity, primerBatch, enzymeBatch, rotorGene, operatorUserId)
        VALUES ('UPDATE NEW',NOW(),NEW.id, NEW.batchCode, NEW.robot, NEW.pcrMachine, NEW.temperature, NEW.datetime, NEW.userId, NEW.version_id, NEW.plateName, NEW.halfPlate, NEW.humidity, NEW.primerBatch, NEW.enzymeBatch, NEW.rotorGene, NEW.operatorUserId);
    END
;

DROP TRIGGER trg_batch_delete;
CREATE TRIGGER trg_batch_delete AFTER DELETE ON batch
    FOR EACH ROW
    BEGIN
        INSERT INTO batch_audit(audit_action, audit_datetime, batchId, batchCode, robot, pcrMachine, temperature, datetime, userId, version_id, plateName, halfPlate, humidity, primerBatch, enzymeBatch, rotorGene, operatorUserId)
        VALUES ('DELETE OLD',NOW(),OLD.id, OLD.batchCode, OLD.robot, OLD.pcrMachine, OLD.temperature, OLD.datetime, OLD.userId, OLD.version_id, OLD.plateName, OLD.halfPlate, OLD.humidity, OLD.primerBatch, OLD.enzymeBatch, OLD.rotorGene, OLD.operatorUserId);
    END
;
