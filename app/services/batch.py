from flask import flash
from flask_login import current_user
from app import db
from app.model.batch import Batch

class BatchService():

    def SaveAndReturn(self, batchForm):
        if (self.BatchCodeIsDuplicate(batchCode=batchForm.batchCode.data)):
            return False

        batch = Batch(
            batchCode = batchForm.batchCode.data,
            robot = batchForm.robot.data,
            pcrMachine = batchForm.pcrMachine.data,
            temperature = batchForm.temperature.data,
            datetime = batchForm.datetime.data,
            userId = current_user.id
            )

        db.session.add(batch)
        db.session.flush()

        return batch

    def BatchCodeIsDuplicate(self, batchCode, excludingId=None):
        existingBatch = Batch.query.filter(Batch.batchCode == batchCode).filter(Batch.id != excludingId).first()

        if (existingBatch):
            flash("Batch Code already exists", "error")
            return True
        else:
            return False
