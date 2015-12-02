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
    COL_BATCH_CODE = 'BatchId'
    COL_ROBOT = 'Robot'
    COL_TEMPERATURE = 'Temperature'
    COL_DATE_PROCESSED = 'DateProcessed'
    COL_UPLOADED_BY = 'Uploaded By'
    COL_PLATE_NAME = 'Plate Name'
    COL_HALF_PLATE = 'Half Plate'
    COL_OPERATOR = 'Operator'
    COL_PRIMER_BATCH = 'Primer Batch'
    COL_ENZYME_BATCH = 'Enzyme Batch'
    COL_ROTOR_GENE = 'Rotor Gene'
    COL_HUMIDITY = 'Humidity'
    COL_SAMPLE_CODE = 'Sample Code'
    COL_WELL = 'Well'
    COL_CONDITION_DESCRIPTION = 'Condition'
    COL_DNA_TEST = 'DNA Test'
    COL_PICO_TEST = 'PICO Test'
    COL_VOLUME = 'Volume'
    COL_ERROR_CODE = 'Error Code'
    COL_T_TO = 't_to'
    COL_T_AMP = 't_amp'
    COL_T = 't'
    COL_S_TO = 's_to'
    COL_S_AMP = 's_amp'
    COL_S = 's'
    COL_TS = 'ts'

    fieldnames = [
        COL_BATCH_CODE,
        COL_ROBOT,
        COL_TEMPERATURE,
        COL_DATE_PROCESSED,
        COL_UPLOADED_BY,
        COL_PLATE_NAME,
        COL_HALF_PLATE,
        COL_OPERATOR,
        COL_PRIMER_BATCH,
        COL_ENZYME_BATCH,
        COL_ROTOR_GENE,
        COL_HUMIDITY,
        COL_SAMPLE_CODE,
        COL_WELL,
        COL_CONDITION_DESCRIPTION,
        COL_DNA_TEST,
        COL_PICO_TEST,
        COL_VOLUME,
        COL_ERROR_CODE,
        COL_T_TO,
        COL_T_AMP,
        COL_T,
        COL_S_TO,
        COL_S_AMP,
        COL_S,
        COL_TS
        ]

    output = csv.DictWriter(outputFile, fieldnames=fieldnames)

    output.writer.writerow(output.fieldnames)

    for measurement in Measurement.query:
        output.writerow({
            COL_BATCH_CODE : measurement.batch.id,
            COL_ROBOT : measurement.batch.robot,
            COL_TEMPERATURE : measurement.batch.temperature,
            COL_DATE_PROCESSED : measurement.batch.datetime,
            COL_UPLOADED_BY : measurement.batch.user.username,
            COL_PLATE_NAME : measurement.batch.plateName,
            COL_HALF_PLATE : measurement.batch.halfPlate,
            COL_OPERATOR : measurement.batch.operator.username,
            COL_PRIMER_BATCH : measurement.batch.primerBatch,
            COL_ENZYME_BATCH : measurement.batch.enzymeBatch,
            COL_ROTOR_GENE : measurement.batch.rotorGene,
            COL_HUMIDITY : measurement.batch.humidity,
            COL_SAMPLE_CODE : measurement.sample.sampleCode,
            COL_WELL : measurement.sample.well,
            COL_CONDITION_DESCRIPTION : measurement.sample.conditionDescription,
            COL_DNA_TEST : measurement.sample.dnaTest,
            COL_PICO_TEST : measurement.sample.picoTest,
            COL_VOLUME : measurement.sample.volume,
            COL_ERROR_CODE : measurement.errorCode,
            COL_T_TO : measurement.t_to,
            COL_T_AMP : measurement.t_amp,
            COL_T : measurement.t,
            COL_S_TO : measurement.s_to,
            COL_S_AMP : measurement.s_amp,
            COL_S : measurement.s,
            COL_TS : measurement.ts
            })