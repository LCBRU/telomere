import datetime
from flask import flash
from flask_login import current_user
from app import db
from app.model.batch import Batch
from app.model.outstandingError import OutstandingError
from app.model.completedError import CompletedError
import numpy
from sets import Set

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

    def GetValidationErrors(self, batch):
        result = []

        for m in batch.measurements:
            errorDescs = Set()

            if m.t_to is None:
                errorDescs.add(self._missingErrorDescription('t_to'))
            elif m.t_to < 12.4 and str(m.errorCode) != '2':
                errorDescs.add("Measurement has T_TO value of {:.2f}, but does not have error code of '2'".format(m.t_to))
            elif m.t_to >= 12.4 and str(m.errorCode) == '2':
                errorDescs.add("Measurement has T_TO value of {:.2f}, but has been given an error code of '2'".format(m.t_to))
            elif m.t_to < 12.4 and str(m.errorCode) == '2':
                errorDescs.add("Validated error code '2': T_TO = {:.2f}.".format(m.t_to))

            if m.t_amp is None:
                errorDescs.add(self._missingErrorDescription('t_amp'))

            if m.t is None:
                errorDescs.add(self._missingErrorDescription('t'))

            if m.s_to is None:
                errorDescs.add(self._missingErrorDescription('s_to'))

            if m.s_amp is None:
                errorDescs.add(self._missingErrorDescription('s_amp'))

            if m.s is None:
                errorDescs.add(self._missingErrorDescription('s'))

            tsValues = [ x.ts for x in batch.get_measurements_for_sample_code(m.sample.sampleCode)]

            if len(tsValues) != 2:
                errorDescs.add("Sample should have 2 measurements in the batch, but instead has %d" % len(tsValues))
            else:
                cv = numpy.std(tsValues, ddof=1) / numpy.mean(tsValues) * 100

                if cv > 10 and str(m.errorCode) != '1':
                    errorDescs.add("Samples have a covariance of {:.2f}, but do not have an error code of '1'".format(cv))
                elif cv <= 10 and str(m.errorCode) == '1':
                    errorDescs.add("Samples have a covariance of {:.2f}, but have been given an error code of '1'".format(cv))
                elif cv > 10 and str(m.errorCode) == '1':
                    errorDescs.add("Validated error code '1': Sample covariance = {:.2f}".format(cv))

            for ed in errorDescs:
                result.append(OutstandingError(
                    description = ed,
                    batchId = batch.id,
                    sampleId = m.sample.id
                    ))

        return result

    def _missingErrorDescription(self, fieldname):
        return "'%s' is missing or not valid" % fieldname