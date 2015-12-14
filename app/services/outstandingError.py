import datetime
from flask_login import current_user
from app import db
from app.model.outstandingError import OutstandingError
from app.model.completedError import CompletedError

class OutstandingErrorService():

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
