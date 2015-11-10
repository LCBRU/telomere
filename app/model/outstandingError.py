from app import db

class OutstandingError(db.Model):

    __tablename__ = 'outstandingError'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200))
    batchId = db.Column(db.Integer, db.ForeignKey('batch.id'))
    sampleId = db.Column(db.Integer, db.ForeignKey('sample.id'))

    batch = db.relationship("Batch", backref=db.backref('outstandingErrors', order_by=id, cascade="all, delete-orphan"))
    sample = db.relationship("Sample", backref=db.backref('outstandingErrors', order_by=id, cascade="all, delete-orphan"))

    def __init__(self, *args, **kwargs):
        self.id = kwargs.get('id')
        self.description = kwargs.get('description')
        self.batchId = kwargs.get('batchId')
        self.sampleId = kwargs.get('sampleId')
