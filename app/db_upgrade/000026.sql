ALTER TABLE batch
      DROP COLUMN primerBatch
    , DROP COLUMN enzymeBatch
    , DROP COLUMN rotorGene
    , DROP COLUMN humidity
;

ALTER TABLE batch
      ADD primerBatch INTEGER NOT NULL
    , ADD enzymeBatch INTEGER NOT NULL
    , ADD rotorGene INTEGER NOT NULL
    , ADD humidity INTEGER NOT NULL
;

ALTER TABLE batch_audit
      DROP COLUMN primerBatch
    , DROP COLUMN enzymeBatch
    , DROP COLUMN rotorGene
    , DROP COLUMN humidity
;

ALTER TABLE batch_audit
      ADD primerBatch INTEGER NOT NULL
    , ADD enzymeBatch INTEGER NOT NULL
    , ADD rotorGene INTEGER NOT NULL
    , ADD humidity INTEGER NOT NULL
;
