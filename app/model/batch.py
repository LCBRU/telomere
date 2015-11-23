from app import db
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql import select, func
from app.model.outstandingError import OutstandingError

class Batch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    robot = db.Column(db.String(20))
    pcrMachine = db.Column(db.String(20))
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
    failed = db.Column(db.Boolean)

    __mapper_args__ = {
        "version_id_col": version_id
    }

    def __init__(self, *args, **kwargs):
        self.id = kwargs.get('id')
        self.robot = kwargs.get('robot')
        self.pcrMachine = kwargs.get('pcrMachine')
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
        self.failed = kwargs.get('failed')

    @hybrid_property
    def outstandingErrorCount(self):
        return len(self.outstandingErrors)

    @outstandingErrorCount.expression
    def outstandingErrorCount(cls):
        return (select([func.count(OutstandingError.id)]).
                where(OutstandingError.batchId == cls.id).
                label("outstandingErrorCount")
                )