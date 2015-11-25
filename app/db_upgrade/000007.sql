ALTER TABLE spreadsheet
    ADD filepath VARCHAR(500)
;

ALTER TABLE spreadsheet
ADD CONSTRAINT uc_spreadsheet_filepath UNIQUE (filepath)
;