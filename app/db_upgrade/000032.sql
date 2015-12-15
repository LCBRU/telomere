ALTER TABLE batch
    DROP COLUMN failed
;

ALTER TABLE batch_audit
    DROP COLUMN failed
;

ALTER TABLE batch
    ADD failed INTEGER NULL
;

ALTER TABLE batch_audit
    ADD failed INTEGER NULL
;
