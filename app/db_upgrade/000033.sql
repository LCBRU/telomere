ALTER TABLE batch
    DROP COLUMN failed
;

ALTER TABLE batch_audit
    DROP COLUMN failed
;

ALTER TABLE batch
    ADD batchFailureReason INTEGER NULL
;

ALTER TABLE batch_audit
    ADD batchFailureReason INTEGER NULL
;

DROP TRIGGER trg_batch_insert;
CREATE TRIGGER trg_batch_insert AFTER INSERT ON batch
    FOR EACH ROW
    BEGIN
        INSERT INTO batch_audit(audit_action, audit_datetime, batchId, robot, temperature, datetime, userId, version_id, plateName, halfPlate, humidity, primerBatch, enzymeBatch, rotorGene, operatorUserId, batchFailureReason)
        VALUES ('INSERT NEW',NOW(),NEW.id, NEW.robot, NEW.temperature, NEW.datetime, NEW.userId, NEW.version_id, NEW.plateName, NEW.halfPlate, NEW.humidity, NEW.primerBatch, NEW.enzymeBatch, NEW.rotorGene, NEW.operatorUserId, NEW.batchFailureReason);
    END
;

DROP TRIGGER trg_batch_update;
CREATE TRIGGER trg_batch_update AFTER UPDATE ON batch
    FOR EACH ROW
    BEGIN
        INSERT INTO batch_audit(audit_action, audit_datetime, batchId, robot, temperature, datetime, userId, version_id, plateName, halfPlate, humidity, primerBatch, enzymeBatch, rotorGene, operatorUserId, batchFailureReason)
        VALUES ('UPDATE OLD',NOW(),OLD.id, OLD.robot, OLD.temperature, OLD.datetime, OLD.userId, OLD.version_id, OLD.plateName, OLD.halfPlate, OLD.humidity, OLD.primerBatch, OLD.enzymeBatch, OLD.rotorGene, OLD.operatorUserId, OLD.batchFailureReason);
        INSERT INTO batch_audit(audit_action, audit_datetime, batchId, robot, temperature, datetime, userId, version_id, plateName, halfPlate, humidity, primerBatch, enzymeBatch, rotorGene, operatorUserId, batchFailureReason)
        VALUES ('UPDATE NEW',NOW(),NEW.id, NEW.robot, NEW.temperature, NEW.datetime, NEW.userId, NEW.version_id, NEW.plateName, NEW.halfPlate, NEW.humidity, NEW.primerBatch, NEW.enzymeBatch, NEW.rotorGene, NEW.operatorUserId, NEW.batchFailureReason);
    END
;

DROP TRIGGER trg_batch_delete;
CREATE TRIGGER trg_batch_delete AFTER DELETE ON batch
    FOR EACH ROW
    BEGIN
        INSERT INTO batch_audit(audit_action, audit_datetime, batchId, robot, temperature, datetime, userId, version_id, plateName, halfPlate, humidity, primerBatch, enzymeBatch, rotorGene, operatorUserId, batchFailureReason)
        VALUES ('DELETE OLD',NOW(),OLD.id, OLD.robot, OLD.temperature, OLD.datetime, OLD.userId, OLD.version_id, OLD.plateName, OLD.halfPlate, OLD.humidity, OLD.primerBatch, OLD.enzymeBatch, OLD.rotorGene, OLD.operatorUserId, OLD.batchFailureReason);
    END
;
