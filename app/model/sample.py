from app import db

class Sample(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sampleCode = db.Column(db.String(20))
    volume = db.Column(db.Numeric(precision=3, scale=1))
    concentration = db.Column(db.Numeric(precision=3, scale=1))
    plateId = db.Column(db.String(20))

    def __init__(self, *args, **kwargs):
        self.id = kwargs.get('id')
        self.sampleCode = kwargs.get('sampleCode')
        self.volume = kwargs.get('volume')
        self.concentration = kwargs.get('concentration')
        self.plateId = kwargs.get('plateId')
