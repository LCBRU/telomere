from app import db

class Batch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    robot = db.Column(db.String(20))

    def __init__(self, *args, **kwargs):
        self.id = kwargs.get('id')
        self.name = kwargs.get('name')
        self.robot = kwargs.get('robot')
