from app import db

class Sample(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sampleId = db.Column(db.String(20))

    def __init__(self, *args, **kwargs):
        self.id = kwargs.get('id')
        self.batchId = kwargs.get('sampleId')
