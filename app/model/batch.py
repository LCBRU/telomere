from app import db

class Batch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500))

    def __init__(self, *args, **kwargs):
        self.id = kwargs.get('id')
        self.details = kwargs.get('name')
