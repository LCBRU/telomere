import datetime
from flask import flash
from flask_login import current_user
from app import db
from app.model.batch import Batch
from app.model.outstandingError import OutstandingError
from app.model.completedError import CompletedError
import numpy
from sets import Set
from decimal import *

class BatchService():

    def SaveAndReturn(self, batchForm):
        batch = Batch(
            robot = batchForm.robot.data,
            pcrMachine = batchForm.pcrMachine.data,
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
            failed = batchForm.failed.data
            )

        db.session.add(batch)
        db.session.flush()

        return batch

    def IsBatchDuplicate(self, batch):
        return (Batch
            .query
            .filter_by(plateName=batch.plateName, halfPlate=batch.halfPlate)
            .filter(Batch.id != batch.id)
            .count()
            ) > 0

    def CompleteError(self, outstandingError):
        ce = CompletedError(
            description = outstandingError.description,
            batchId = outstandingError.batchId,
            sampleId = outstandingError.sampleId,
            completedByUserId = current_user.id,
            completedDatetime = datetime.datetime.now()
            )

        db.session.add(ce)
        db.session.delete(outstandingError)

    def CompleteAllErrors(self, batch):
        for oe in batch.outstandingErrors:
            self.CompleteError(oe)

    def SetCoefficientsOfVariation(self, batch):
        for m in batch.measurements:
            tsValues = [ x.ts for x in batch.get_measurements_for_sample_code(m.sample.sampleCode)]

            m.errorInvalidSampleCount = False
            m.errorHighCv = False

            if len(tsValues) != 2:
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
