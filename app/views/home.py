from flask import g, render_template, send_file
from flask.ext.login import login_required
import tempfile, os, csv, datetime

from app import telomere, db

from app.model.batch import Batch
from app.model.sample import Sample
from app.model.measurement import Measurement

@telomere.route('/')
def index():
	batches = Batch.query.count()
	samples = Sample.query.count()
	measurements = Measurement.query.count()

	return render_template('index.html', batches=batches, samples=samples, measurements=measurements)

@telomere.route('/export')
def export():
    f = tempfile.TemporaryFile()

    try:
        _writeCsv(f)

        f.seek(0)
        response = send_file(f, as_attachment=True, attachment_filename="telomere_%s.csv" % datetime.datetime.now().strftime('%Y%M%d%H%m%S'),
                             add_etags=False)
        f.seek(0, os.SEEK_END)
        size = f.tell()
        f.seek(0)
        response.headers.extend({
            'Content-Length': size,
            'Cache-Control': 'no-cache'
        })
        
        return response
    
    finally:
	    f.close

def _writeCsv(outputFile):
    COL_BATCH_CODE = 'BatchCode'
    COL_ROBOT = 'Robot'
    COL_PCR_MACHINE = 'PcrMachine'
    COL_TEMPERATURE = 'Temperature'
    COL_DATE_PROCESSED = 'DateProcessed'
    COL_SAMPLE_CODE = 'Sample Code'
    COL_T1 = 't1'
    COL_S1 = 's1'
    COL_T2 = 't2'
    COL_S2 = 's2'

    fieldnames = [
        COL_BATCH_CODE,
        COL_ROBOT,
        COL_PCR_MACHINE,
        COL_TEMPERATURE,
        COL_DATE_PROCESSED,
        COL_SAMPLE_CODE,
        COL_T1,
        COL_S1,
        COL_T2,
        COL_S2]

    output = csv.DictWriter(outputFile, fieldnames=fieldnames)

    output.writer.writerow(output.fieldnames)

    for batch in Batch.query.order_by(Batch.datetime.asc()):
    	for measurement in batch.measurements:
            output.writerow({
                COL_BATCH_CODE : batch.batchCode,
                COL_ROBOT : batch.robot,
                COL_PCR_MACHINE: batch.pcrMachine,
                COL_TEMPERATURE: batch.temperature,
                COL_DATE_PROCESSED: batch.datetime,
                COL_SAMPLE_CODE: measurement.sample.sampleCode,
                COL_T1: measurement.t1,
                COL_S1: measurement.s1,
                COL_T2: measurement.t2,
                COL_S2: measurement.s2
                })
