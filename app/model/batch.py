from app import db

class Batch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    batchId = db.Column(db.String(20))
    robot = db.Column(db.String(20))
    pcrMachine = db.Column(db.String(20))
    temperature = db.Column(db.Numeric(precision=3, scale=1))
    datetime = db.Column(db.DateTime())
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, *args, **kwargs):
        self.id = kwargs.get('id')
        self.batchId = kwargs.get('batchId')
        self.robot = kwargs.get('robot')
        self.pcrMachine = kwargs.get('pcrMachine')
        self.temperature = kwargs.get('temperature')
        self.datetime = kwargs.get('datetime')
        self.userId = kwargs.get('userId')
