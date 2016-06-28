UPDATE measurement m
JOIN    batch b ON b.id = m.batchId
                AND b.primerBatch = 3
SET errorLowT_to = 0
WHERE m.errorLowT_to = 1
    AND m.t_to >= 11.7
;

DELETE oe
FROM    outstandingError oe
JOIN    measurement m ON m.batchId = oe.batchId
                    AND m.sampleId = oe.sampleId
                    AND m.errorLowT_to = 0
                    AND m.t_to < 12.4
JOIN    batch b ON b.id = m.batchId
                AND b.primerBatch = 3
WHERE   oe.description LIKE 'Measurement has T_TO value of%but does not have%'
;