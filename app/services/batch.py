from flask import flash
from flask_login import current_user
from app import db
from app.model.batch import Batch

class BatchService():

    def SaveAndReturn(self, batchForm):
        batch = Batch.query.filter_by(batchCode=batchForm.batchCode.data).first()

        if (batch):
            flash("Batch Code already exists", "error")
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

