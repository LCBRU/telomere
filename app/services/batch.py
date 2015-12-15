import datetime
from flask import flash
from flask_login import current_user
from app import db
from app.model.batch import Batch
from app.model.outstandingError import OutstandingError
import numpy
from sets import Set
from decimal import *

class BatchService():

    def SaveAndReturn(self, batchForm):
        batch = Batch(
            robot = batchForm.robot.data,
            temperature = batchForm.temperature.data,
            datetime = batchForm.datetime.data,
            userId = current_user.id,
            plateName = batchForm.plateName.data,
            halfPlate = batchForm.halfPlate.data,
            humidity = batchForm.humidity.data,
            primerBatch = batchForm.primerBatch.data,
            enzymeBatch = batchForm.enzymeBatch.data,
            rotorGene = batchForm.rotorGene.data,
            operatorUserId = batchForm.operatorUserId.data,
            batchFailureReason = batchForm.batchFailureReason.data,
            processType = batchForm.processType.data
            )

        db.session.add(batch)
        db.session.flush()

        return batch

    def IsBatchDuplicate(self, batch):
        return (Batch
            .query
            .filter_by(plateName=batch.plateName)
            .filter_by(halfPlate=batch.halfPlate)
            .filter(Batch.id != batch.id)
            .count()
            ) > 0

    def SetCoefficientsOfVariation(self, batch):
        for m in batch.measurements:
            measurements = batch.get_measurements_for_sample_code(m.sample.sampleCode)
            
            tsValues = [ x.ts for x in measurements if x.ts is not None]

            m.errorInvalidSampleCount = False
            m.errorHighCv = False

            if not m.sample.is_valid_measurement_count(len(tsValues)):
                m.errorInvalidSampleCount = True
                continue

            m.coefficientOfVariation = round(numpy.std(tsValues, ddof=1) / numpy.mean(tsValues) * 100, 6)
            m.errorHighCv = m.coefficientOfVariation > 10

    def GetValidationErrors(self, batch):
        result = []

        for m in batch.measurements:
            for ed in m.GetValidationErrors():
                result.append(OutstandingError(
                    description = ed,
                    batchId = batch.id,
                    sampleId = m.sample.id
                    ))

        return result
