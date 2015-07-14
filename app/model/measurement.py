from app import db

class Measurement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    batchId = db.Column(db.Integer, db.ForeignKey('batch.id'))
    sampleId = db.Column(db.Integer, db.ForeignKey('sample.id'))
    t1 = db.Column(db.Numeric(precision=5, scale=2))
    s1 = db.Column(db.Numeric(precision=5, scale=2))
    t2 = db.Column(db.Numeric(precision=5, scale=2))
    s2 = db.Column(db.Numeric(precision=5, scale=2))
    tsRatio = db.Column(db.Numeric(precision=5, scale=2))

    def __init__(self, *args, **kwargs):
        self.id = kwargs.get('id')
        self.batchId = kwargs.get('batchId')
        self.sampleId = kwargs.get('sampleId')
        self.t1 = kwargs.get('t1')
        self.s1 = kwargs.get('s1')
        self.t2 = kwargs.get('t2')
        self.s2 = kwargs.get('s2')
        self.tsRatio = kwargs.get('tsRatio')
