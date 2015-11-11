from app import db

class CompletedError(db.Model):

    __tablename__ = 'completedError'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200))
    batchId = db.Column(db.Integer, db.ForeignKey('batch.id'))
    sampleId = db.Column(db.Integer, db.ForeignKey('sample.id'))
    completedByUserId = db.Column(db.Integer, db.ForeignKey('user.id'))
    completedDatetime = db.Column(db.DateTime())

    batch = db.relationship("Batch", backref=db.backref('completedErrors', order_by=id, cascade="all, delete-orphan"))
    sample = db.relationship("Sample", backref=db.backref('completedErrors', order_by=id, cascade="all, delete-orphan"))
    completedByUser = db.relationship("User", backref=db.backref('completedErrors', order_by=id, cascade="all, delete-orphan"))

    def __init__(self, *args, **kwargs):
        self.id = kwargs.get('id')
        self.description = kwargs.get('description')
        self.batchId = kwargs.get('batchId')
        self.sampleId = kwargs.get('sampleId')
        self.completedByUserId = kwargs.get('completedByUserId')
        self.completedDatetime = kwargs.get('completedDatetime')
