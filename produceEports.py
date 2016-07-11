#!/usr/bin/env python
from app.views.export import write_all_measurements_csv
from app import db
from sqlalchemy.sql import text
import os

exportDirectory = "{0}/app/static/exports".format(os.path.dirname(os.path.realpath(__file__)))
workingFile = "/tmp/AllMeasurements_inprogress.csv"
finalFile = "{0}/AllMeasurements.csv".format(exportDirectory)

cmd = """
    SELECT
          b.id AS batchId
        , b.processType
        , b.robot
        , b.temperature
        , b.datetime
        , u.username
        , b.plateName
        , b.halfPlate
        , o.username AS operator_name
        , o.code AS operator_code
        , b.primerBatch
        , b.enzymeBatch
        , b.rotorGene
        , b.humidity
        , s.sampleCode
        , m.errorCode
        , m.t_to
        , m.t_amp
        , m.t
        , m.s_to
        , m.s_amp
        , m.s
        , m.ts
        , m.coefficientOfVariation
        , m.errorLowT_to
        , m.errorHighCv
        , m.errorInvalidSampleCount
    FROM    measurement m
    JOIN    batch b ON b.id = m.batchId
    JOIN    sample s ON s.id = m.sampleId
    JOIN    user u ON u.id = b.userId
    JOIN    user o ON o.id = b.operatorUserId
    INTO OUTFILE '/tmp/AllMeasurements_inprogress.csv'
    FIELDS TERMINATED BY ','
    ENCLOSED BY '"'
    LINES TERMINATED BY '\n';
"""

db.engine.execute(text(cmd))

os.rename(workingFile, finalFile)

