from flask import flash
from flask_login import current_user
from app import db
from app.model.sample import Sample

class SampleService():

    def GetOrCreateSample(self, sampleCode):
        sample = Sample.query.filter_by(sampleCode=sampleCode).first()

        if (not sample):
            sample = Sample(sampleCode=sampleCode)
            db.session.add(sample)
            db.session.flush()
        else:
            flash("Duplicate measurement for sample '%s' recorded." % sampleCode)

        return sample
