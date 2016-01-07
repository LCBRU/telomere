from app import db

class Sample(db.Model):
    POOL_NAME = 'pool'

    id = db.Column(db.Integer, primary_key=True)
    sampleCode = db.Column(db.String(20))

    def __init__(self, *args, **kwargs):
        self.id = kwargs.get('id')
        self.sampleCode = kwargs.get('sampleCode')

    def is_pool_sample(self):
        return self.sampleCode == Sample.POOL_NAME

    def plate_name_mismatch(self, plateName):
        if self.is_pool_sample():
            return False

        return plateName not in [p.plateName for p in self.samplePlates]

    def get_samplePlate_for_plateName(self, plate_name):
        return next((p for p in self.samplePlates if p.plateName == plate_name), None)

    def is_valid_measurement_count(self, num_values):
        if self.is_pool_sample():
            return (num_values == 3 or num_values == 4)
        else:
            return num_values == 2