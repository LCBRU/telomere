from app import db

class Measurement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    batchId = db.Column(db.Integer, db.ForeignKey('batch.id'))
    sampleId = db.Column(db.Integer, db.ForeignKey('sample.id'))
    t_to = db.Column(db.Numeric(precision=6, scale=2))
    t_amp = db.Column(db.Numeric(precision=6, scale=2))
    t = db.Column(db.Numeric(precision=6, scale=3))
    s_to = db.Column(db.Numeric(precision=6, scale=2))
    s_amp = db.Column(db.Numeric(precision=6, scale=2))
    s = db.Column(db.Numeric(precision=6, scale=3))
    ts = db.Column(db.Numeric(precision=12, scale=6))
    errorCode = db.Column(db.String(50))


    batch = db.relationship("Batch", backref=db.backref('measurements', order_by=id, cascade="all, delete-orphan"))
    sample = db.relationship("Sample", backref=db.backref('measurements', order_by=id, cascade="all, delete-orphan"))

    def __init__(self, *args, **kwargs):
        self.id = kwargs.get('id')
        self.batchId = kwargs.get('batchId')
        self.sampleId = kwargs.get('sampleId')
        self.t_to = kwargs.get('t_to')
        self.t_amp = kwargs.get('t_amp')
        self.t = kwargs.get('t')
        self.s_to = kwargs.get('s_to')
        self.s_amp = kwargs.get('s_amp')
        self.s = kwargs.get('s')
        self.errorCode = kwargs.get('errorCode')
        self.ts = self.t / self.s
