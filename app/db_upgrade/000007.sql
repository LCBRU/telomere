ALTER TABLE spreadsheet
    ADD filepath VARCHAR(1000)
;

ALTER TABLE spreadsheet
ADD CONSTRAINT uc_spreadsheet_filepath UNIQUE (filepath)
;