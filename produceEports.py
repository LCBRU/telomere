#!/usr/bin/env python
from app import db
from sqlalchemy.sql import text
import os
import tempfile

temp_name = next(tempfile._get_candidate_names())
exportDirectory = "{0}/app/static/exports".format(
    os.path.dirname(os.path.realpath(__file__)))
workingFile = "/db/mysql/tmp/{0}.csv".format(temp_name)
finalFile = "{0}/AllMeasurements.csv".format(exportDirectory)

cmd = """
          SELECT
          'batchId'
        , 'processType'
        , 'robot'
        , 'temperature'
        , 'datetime'
        , 'username'
        , 'plateName'
        , 'halfPlate'
        , 'operator_name'
        , 'operator_code'
        , 'primerBatch'
        , 'enzymeBatch'
        , 'rotorGene'
        , 'humidity'
        , 'sampleCode'
        , 'errorCode'
        , 't_to'
        , 't_amp'
        , 't'
        , 's_to'
        , 's_amp'
        , 's'
        , 'ts'
        , 'coefficientOfVariation'
        , 'errorLowT_to'
        , 'errorHighCv'
        , 'errorInvalidSampleCount'
UNION ALL
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
    INTO OUTFILE '{0}'
    FIELDS TERMINATED BY ','
    ENCLOSED BY '"'
    LINES TERMINATED BY '\n';
""".format(workingFile)

db.engine.execute(text(cmd))
