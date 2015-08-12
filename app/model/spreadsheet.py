from app import db

class Spreadsheet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(500))
    uploaded = db.Column(db.DateTime())
    processed = db.Column(db.DateTime())
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))
    batchId = db.Column(db.Integer, db.ForeignKey('batch.id'))
    user = db.relationship("User")
    batch = db.relationship("Batch")

    def __init__(self, *args, **kwargs):
        self.id = kwargs.get('id')
        self.filename = kwargs.get('filename')
        self.uploaded = kwargs.get('uploaded')
        self.processed = kwargs.get('processed')
        self.userId = kwargs.get('userId')
        self.batchId = kwargs.get('batchId')
