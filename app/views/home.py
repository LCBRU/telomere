from flask import g, render_template
from flask.ext.login import login_required

from app import telomere

from app.model.batch import Batch
from app.model.sample import Sample
from app.model.measurement import Measurement

@telomere.route('/')
def index():
	batches = Batch.query.count()
	samples = Sample.query.count()
	measurements = Measurement.query.count()

	return render_template('index.html', batches=batches, samples=samples, measurements=measurements)
