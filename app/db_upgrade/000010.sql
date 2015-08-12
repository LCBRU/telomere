ALTER TABLE spreadsheet
      ADD batchId INTEGER NOT NULL
;

ALTER TABLE spreadsheet
    ADD CONSTRAINT fk_spreadsheet_batch FOREIGN KEY (batchId) REFERENCES batch(Id)
;