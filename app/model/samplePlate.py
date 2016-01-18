from app import db

class SamplePlate(db.Model):

    __tablename__ = 'samplePlate'

    id = db.Column(db.Integer, primary_key=True)
    sampleCode = db.Column(db.String(20), db.ForeignKey('sample.sampleCode'))
    volume = db.Column(db.Integer)
    plateName = db.Column(db.String(50))
    well = db.Column(db.String(50))
    conditionDescription = db.Column(db.String(50))
    dnaTest = db.Column(db.Numeric(precision=6, scale=2), nullable=True)
    picoTest = db.Column(db.Numeric(precision=6, scale=2), nullable=True)
    manifestId = db.Column(db.Integer, db.ForeignKey('manifest.id'))

    manifest = db.relationship("Manifest", backref=db.backref('samplePlates', order_by=id, cascade="all, delete-orphan"))
    sample = db.relationship("Sample", backref=db.backref('samplePlates', order_by=id, cascade="all, delete-orphan"))

    def __init__(self, *args, **kwargs):
        self.id = kwargs.get('id')
        self.sampleId = kwargs.get('sampleId')
        self.volume = kwargs.get('volume')
        self.plateName = kwargs.get('plateName')
        self.well = kwargs.get('well')
        self.conditionDescription = kwargs.get('conditionDescription')
        self.dnaTest = kwargs.get('dnaTest')
        self.picoTest = kwargs.get('picoTest')
        self.manifestId = kwargs.get('manifestId')
