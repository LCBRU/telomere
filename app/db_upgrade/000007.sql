ALTER TABLE spreadsheet
    ADD filepath VARCHAR(200)
;

ALTER TABLE spreadsheet
ADD CONSTRAINT uc_spreadsheet_filepath UNIQUE (filepath)
;