ALTER TABLE spreadsheet
    DROP filepath
;

ALTER TABLE spreadsheet
DROP UNIQUE uc_spreadsheet_filepath
;