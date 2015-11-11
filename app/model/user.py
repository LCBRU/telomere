from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    code = db.Column(db.String(10))
    batchesEntered = db.relationship("Batch", foreign_keys="[Batch.userId]", backref="user")
    batchesProcessed = db.relationship("Batch", foreign_keys="[Batch.operatorUserId]", backref="operator")
 
    def __init__(self, username):
        self.username = username
 
    def is_authenticated(self):
        return True
 
    def is_active(self):
        return True
 
    def is_anonymous(self):
        return False
 
    def get_id(self):
        return unicode(self.id)

    def GetCodeAndName(self):
        return "%s - %s" % (self.code, self.username)

