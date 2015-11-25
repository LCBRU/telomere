ALTER TABLE measurement
      ADD errorLowT_to BOOLEAN NULL
    , ADD errorHighCv BOOLEAN NULL
    , ADD coefficientOfVariation DECIMAL(12,6) NULL
    , ADD errorInvalidSampleCount BOOLEAN NULL
;

ALTER TABLE measurement_audit
      ADD errorLowT_to BOOLEAN NULL
    , ADD errorHighCv BOOLEAN NULL
    , ADD coefficientOfVariation DECIMAL(12,6) NULL
    , ADD errorInvalidSampleCount BOOLEAN NULL
;

DROP TRIGGER trg_measurement_insert;
CREATE TRIGGER trg_measurement_insert AFTER INSERT ON measurement
    FOR EACH ROW
    BEGIN
        INSERT INTO measurement_audit(audit_action, audit_datetime, measurementId, batchId, sampleId, t_to, t_amp, t, s_to, s_amp, s, ts, errorCode, coefficientOfVariation, errorLowT_to, errorHighCv, errorInvalidSampleCount)
        VALUES ('INSERT NEW',NOW(),NEW.id, NEW.batchId, NEW.sampleId, NEW.t_to, NEW.t_amp, NEW.t, NEW.s_to, NEW.s_amp, NEW.s, NEW.ts, NEW.errorCode, NEW.coefficientOfVariation, NEW.errorLowT_to, NEW.errorHighCv, NEW.errorInvalidSampleCount);
    END
;

DROP TRIGGER trg_measurement_update;
CREATE TRIGGER trg_measurement_update AFTER UPDATE ON measurement
    FOR EACH ROW
    BEGIN
        INSERT INTO measurement_audit(audit_action, audit_datetime, measurementId, batchId, sampleId, t_to, t_amp, t, s_to, s_amp, s, ts, errorCode, coefficientOfVariation, errorLowT_to, errorHighCv, errorInvalidSampleCount)
        VALUES ('UPDATE OLD',NOW(),OLD.id, OLD.batchId, OLD.sampleId, OLD.t_to, OLD.t_amp, OLD.t, OLD.s_to, OLD.s_amp, OLD.s, OLD.ts, OLD.errorCode, OLD.coefficientOfVariation, OLD.errorLowT_to, OLD.errorHighCv, OLD.errorInvalidSampleCount);
        INSERT INTO measurement_audit(audit_action, audit_datetime, measurementId, batchId, sampleId, t_to, t_amp, t, s_to, s_amp, s, ts, errorCode, coefficientOfVariation, errorLowT_to, errorHighCv, errorInvalidSampleCount)
        VALUES ('UPDATE NEW',NOW(),NEW.id, NEW.batchId, NEW.sampleId, NEW.t_to, NEW.t_amp, NEW.t, NEW.s_to, NEW.s_amp, NEW.s, NEW.ts, NEW.errorCode, NEW.coefficientOfVariation, NEW.errorLowT_to, NEW.errorHighCv, NEW.errorInvalidSampleCount);
    END
;

DROP TRIGGER trg_measurement_delete;
CREATE TRIGGER trg_measurement_delete AFTER DELETE ON measurement
    FOR EACH ROW
    BEGIN
        INSERT INTO measurement_audit(audit_action, audit_datetime, measurementId, batchId, sampleId, t_to, t_amp, t, s_to, s_amp, s, ts, errorCode, coefficientOfVariation, errorLowT_to, errorHighCv, errorInvalidSampleCount)
        VALUES ('DELETE OLD',NOW(),OLD.id, OLD.batchId, OLD.sampleId, OLD.t_to, OLD.t_amp, OLD.t, OLD.s_to, OLD.s_amp, OLD.s, OLD.ts, OLD.errorCode, OLD.coefficientOfVariation, OLD.errorLowT_to, OLD.errorHighCv, OLD.errorInvalidSampleCount);
    END
;

