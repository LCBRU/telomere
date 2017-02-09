from flask import g, render_template
from flask_login import login_required

from app import telomere

from app.model.batch import Batch
from app.model.samplePlate import SamplePlate
from app.model.measurement import Measurement
from app.model.manifest import Manifest

@telomere.route('/')
def index():
	manifests = Manifest.query.count()
	batches = Batch.query.count()
	samplePlates = SamplePlate.query.count()
	measurements = Measurement.query.count()

	return render_template('index.html', batches=batches, samplePlates=samplePlates, measurements=measurements, manifests=manifests)
