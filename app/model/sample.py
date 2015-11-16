from app import db

class Sample(db.Model):
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
