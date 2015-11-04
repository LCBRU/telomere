from app import db

class Manifest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(500))
    uploaded = db.Column(db.DateTime())
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User")

    def __init__(self, *args, **kwargs):
        self.id = kwargs.get('id')
        self.filename = kwargs.get('filename')
        self.uploaded = kwargs.get('uploaded')
        self.userId = kwargs.get('userId')
