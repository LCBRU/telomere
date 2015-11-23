from app import db

class Measurement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    batchId = db.Column(db.Integer, db.ForeignKey('batch.id'))
    sampleId = db.Column(db.Integer, db.ForeignKey('sample.id'))
    t_to = db.Column(db.Numeric(precision=6, scale=2), nullable=True)
    t_amp = db.Column(db.Numeric(precision=6, scale=2), nullable=True)
    t = db.Column(db.Numeric(precision=6, scale=3), nullable=True)
    s_to = db.Column(db.Numeric(precision=6, scale=2), nullable=True)
    s_amp = db.Column(db.Numeric(precision=6, scale=2), nullable=True)
    s = db.Column(db.Numeric(precision=6, scale=3), nullable=True)
    ts = db.Column(db.Numeric(precision=12, scale=6), nullable=True)
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

        if self.t is not None and self.s is not None:
            self.ts = self.t / self.s

        self.errorCode = kwargs.get('errorCode')

    def GetErrorDescription(self):
        descs = []

        if self.errorCode != '':
            descs.append("Error Code is '%s'" % self.errorCode)
        if self.t_to is None:
            descs.append(self._missingErrorDescription('t_to'))
        if self.t_amp is None:
            descs.append(self._missingErrorDescription('t_amp'))
        if self.t is None:
            descs.append(self._missingErrorDescription('t'))
        if self.s_to is None:
            descs.append(self._missingErrorDescription('s_to'))
        if self.s_amp is None:
            descs.append(self._missingErrorDescription('s_amp'))
        if self.s is None:
            descs.append(self._missingErrorDescription('s'))

        return "; ".join(str(x) for x in descs)

    def HasErrors(self):
        return len(self.GetErrorDescription()) > 0

    def _missingErrorDescription(self, fieldname):
        return "'%s' is missing or not valid" % fieldname