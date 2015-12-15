from app import db

class Sample(db.Model):
    POOL_NAME = 'pool'

    id = db.Column(db.Integer, primary_key=True)
    sampleCode = db.Column(db.String(20))
    volume = db.Column(db.Numeric(precision=6, scale=2))
    plateName = db.Column(db.String(50))
    well = db.Column(db.String(50))
    conditionDescription = db.Column(db.String(50))
    dnaTest = db.Column(db.Numeric(precision=6, scale=2))
    picoTest = db.Column(db.Numeric(precision=6, scale=2))
    manifestId = db.Column(db.Integer, db.ForeignKey('manifest.id'))

    manifest = db.relationship("Manifest", backref=db.backref('samples', order_by=id, cascade="all, delete-orphan"))

    def __init__(self, *args, **kwargs):
        self.id = kwargs.get('id')
        self.sampleCode = kwargs.get('sampleCode')
        self.volume = kwargs.get('volume')
        self.plateName = kwargs.get('plateName')
        self.well = kwargs.get('well')
        self.conditionDescription = kwargs.get('conditionDescription')
        self.dnaTest = kwargs.get('dnaTest')
        self.picoTest = kwargs.get('picoTest')
        self.manifestId = kwargs.get('manifestId')

    def is_pool_sample(self):
        return self.sampleCode == Sample.POOL_NAME

    def plate_name_mismatch(self, plateName):
        return self.plateName != plateName and not self.is_pool_sample()

    def is_valid_measurement_count(self, num_values):
        if self.is_pool_sample():
            return (num_values == 3 or num_values == 4)
        else:
            return num_values == 2