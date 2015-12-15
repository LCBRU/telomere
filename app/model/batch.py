from app import db
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql import select, func
from app.model.outstandingError import OutstandingError

class Batch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    robot = db.Column(db.String(20))
    temperature = db.Column(db.Numeric(precision=3, scale=1))
    datetime = db.Column(db.DateTime())
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))
    version_id = db.Column(db.Integer, nullable=False)
    plateName = db.Column(db.String(50))
    halfPlate = db.Column(db.String(1))
    humidity = db.Column(db.Integer())
    primerBatch = db.Column(db.Integer())
    enzymeBatch = db.Column(db.Integer())
    rotorGene = db.Column(db.Integer())
    operatorUserId = db.Column(db.Integer, db.ForeignKey('user.id'))
    batchFailureReason = db.Column(db.Integer())
    processType = db.Column(db.String(20))

    __mapper_args__ = {
        "version_id_col": version_id
    }

    def __init__(self, *args, **kwargs):
        self.id = kwargs.get('id')
        self.robot = kwargs.get('robot')
        self.temperature = kwargs.get('temperature')
        self.datetime = kwargs.get('datetime')
        self.userId = kwargs.get('userId')
        self.plateName = kwargs.get('plateName')
        self.halfPlate = kwargs.get('halfPlate')
        self.humidity = kwargs.get('humidity')
        self.primerBatch = kwargs.get('primerBatch')
        self.enzymeBatch = kwargs.get('enzymeBatch')
        self.rotorGene = kwargs.get('rotorGene')
        self.operatorUserId = kwargs.get('operatorUserId')
        self.batchFailureReason = kwargs.get('batchFailureReason')
        self.processType = kwargs.get('processType')

    @hybrid_property
    def outstandingErrorCount(self):
        return len(self.outstandingErrors)

    @outstandingErrorCount.expression
    def outstandingErrorCount(cls):
        return (select([func.count(OutstandingError.id)]).
                where(OutstandingError.batchId == cls.id).
                label("outstandingErrorCount")
                )

    def get_measurements_for_sample_code(self, sampleCode):
        return [m for m in self.measurements if m.sample.sampleCode == sampleCode]

    def is_duplicate(self):
        return self.processType == "Duplicate"

    def is_replate(self):
        return self.processType == "Re-Plate"

    def is_initial(self):
        return self.processType == "Initial"
