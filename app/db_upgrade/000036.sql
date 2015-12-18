ALTER TABLE sample
    DROP COLUMN volume
;

ALTER TABLE sample_audit
    DROP COLUMN volume
;

ALTER TABLE sample
    ADD volume INTEGER NOT NULL
;

ALTER TABLE sample_audit
    ADD volume INTEGER NOT NULL
;
