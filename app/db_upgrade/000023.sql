ALTER TABLE measurement
      DROP COLUMN t_to
    , DROP COLUMN t_amp
    , DROP COLUMN t
    , DROP COLUMN s_to
    , DROP COLUMN s_amp
    , DROP COLUMN s
    , DROP COLUMN ts
;

ALTER TABLE measurement
      ADD t_to DECIMAL(6,2) NULL
    , ADD t_amp DECIMAL(6,2) NULL
    , ADD t DECIMAL(6,3) NULL
    , ADD s_to DECIMAL(6,2) NULL
    , ADD s_amp DECIMAL(6,2) NULL
    , ADD s DECIMAL(6,3) NULL
    , ADD ts DECIMAL(12,6) NULL
;

ALTER TABLE measurement_audit
      DROP COLUMN t_to
    , DROP COLUMN t_amp
    , DROP COLUMN t
    , DROP COLUMN s_to
    , DROP COLUMN s_amp
    , DROP COLUMN s
    , DROP COLUMN ts
;

ALTER TABLE measurement_audit
      ADD t_to DECIMAL(6,2) NULL
    , ADD t_amp DECIMAL(6,2) NULL
    , ADD t DECIMAL(6,3) NULL
    , ADD s_to DECIMAL(6,2) NULL
    , ADD s_amp DECIMAL(6,2) NULL
    , ADD s DECIMAL(6,3) NULL
    , ADD ts DECIMAL(12,6) NULL
;
