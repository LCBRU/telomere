ALTER TABLE measurement
      DROP COLUMN t1
    , DROP COLUMN t2
    , DROP COLUMN s1
    , DROP COLUMN s2
;

ALTER TABLE measurement
      ADD t_to DECIMAL(6,2) NOT NULL
    , ADD t_amp DECIMAL(6,2) NOT NULL
    , ADD t DECIMAL(6,3) NOT NULL
    , ADD s_to DECIMAL(6,2) NOT NULL
    , ADD s_amp DECIMAL(6,2) NOT NULL
    , ADD s DECIMAL(6,3) NOT NULL
    , ADD ts DECIMAL(12,6) NOT NULL
    , ADD errorCode VARCHAR(50) NOT NULL
;

ALTER TABLE measurement_audit
      DROP COLUMN t1
    , DROP COLUMN t2
    , DROP COLUMN s1
    , DROP COLUMN s2
;

ALTER TABLE measurement_audit
      ADD t_to DECIMAL(6,2) NOT NULL
    , ADD t_amp DECIMAL(6,2) NOT NULL
    , ADD t DECIMAL(6,3) NOT NULL
    , ADD s_to DECIMAL(6,2) NOT NULL
    , ADD s_amp DECIMAL(6,2) NOT NULL
    , ADD s DECIMAL(6,3) NOT NULL
    , ADD ts DECIMAL(12,6) NOT NULL
    , ADD errorCode VARCHAR(50) NOT NULL
;

DROP TRIGGER trg_measurement_insert;
CREATE TRIGGER trg_measurement_insert AFTER INSERT ON measurement
    FOR EACH ROW
    BEGIN
        INSERT INTO measurement_audit(audit_action, audit_datetime, measurementId, batchId, sampleId, t_to, t_amp, t, s_to, s_amp, s, ts, errorCode)
        VALUES ('INSERT NEW',NOW(),NEW.id, NEW.batchId, NEW.sampleId, NEW.t_to, NEW.t_amp, NEW.t, NEW.s_to, NEW.s_amp, NEW.s, NEW.ts, NEW.errorCode);
    END
;

DROP TRIGGER trg_measurement_update;
CREATE TRIGGER trg_measurement_update AFTER UPDATE ON measurement
    FOR EACH ROW
    BEGIN
        INSERT INTO measurement_audit(audit_action, audit_datetime, measurementId, batchId, sampleId, t_to, t_amp, t, s_to, s_amp, s, ts, errorCode)
        VALUES ('UPDATE OLD',NOW(),OLD.id, OLD.batchId, OLD.sampleId, OLD.t_to, OLD.t_amp, OLD.t, OLD.s_to, OLD.s_amp, OLD.s, OLD.ts, OLD.errorCode);
        INSERT INTO measurement_audit(audit_action, audit_datetime, measurementId, batchId, sampleId, t_to, t_amp, t, s_to, s_amp, s, ts, errorCode)
        VALUES ('UPDATE NEW',NOW(),NEW.id, NEW.batchId, NEW.sampleId, NEW.t_to, NEW.t_amp, NEW.t, NEW.s_to, NEW.s_amp, NEW.s, NEW.ts, NEW.errorCode);
    END
;

DROP TRIGGER trg_measurement_delete;
CREATE TRIGGER trg_measurement_delete AFTER DELETE ON measurement
    FOR EACH ROW
    BEGIN
        INSERT INTO measurement_audit(audit_action, audit_datetime, measurementId, batchId, sampleId, t_to, t_amp, t, s_to, s_amp, s, ts, errorCode)
        VALUES ('DELETE OLD',NOW(),OLD.id, OLD.batchId, OLD.sampleId, OLD.t_to, OLD.t_amp, OLD.t, OLD.s_to, OLD.s_amp, OLD.s, OLD.ts, OLD.errorCode);
    END
;

