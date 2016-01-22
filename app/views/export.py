from flask import g, send_file, render_template, redirect, url_for
from flask.ext.login import login_required
import tempfile, os, csv, datetime
from flask_login import current_user
from sets import Set

from app import telomere, db

from app.model.batch import Batch
from app.model.measurement import Measurement
from app.model.outstandingError import OutstandingError
from app.model.user import User
from app.model.samplePlate import SamplePlate
from app.forms.export import ExportUserErrorsForm

@telomere.route('/exports')
@login_required
def export_index():
    return render_template('export_index.html')

@telomere.route('/exports/all_measurements')
@login_required
def export_all_measurements():
    f = tempfile.TemporaryFile()

    try:
        _write_all_measurements_csv(f)

        return _send_csv_to_response(f)

    finally:
	    f.close

@telomere.route('/exports/my_errors')
@login_required
def export_my_errors():
    f = tempfile.TemporaryFile()

    try:
        _write_user_errors_csv(f, current_user.id)

        return _send_csv_to_response(f)

    finally:
        f.close

@telomere.route("/exports/user_errors")
@login_required
def export_user_errors():
    form = ExportUserErrorsForm()
    users = User.query.order_by(User.code.asc()).all()
    form.operatorUserId.choices = [(u.id, u.GetCodeAndName()) for u in users]

    return render_template('export/user_errors.html', form=form)

@telomere.route("/exports/user_errors/output/", methods=['POST'])
@login_required
def export_user_errors_output():
    form = ExportUserErrorsForm()
    users = User.query.order_by(User.code.asc()).all()
    form.operatorUserId.choices = [(u.id, u.GetCodeAndName()) for u in users]

    if form.validate_on_submit():

        f = tempfile.TemporaryFile()

        try:
            _write_user_errors_csv(f, form.operatorUserId.data)

            return _send_csv_to_response(f)

        finally:
            f.close

    return redirect(url_for('export_user_errors'))


def _send_csv_to_response(f):
    f.seek(0)
    response = send_file(f, as_attachment=True, attachment_filename="telomere_all_measurements_%s.csv" % datetime.datetime.now().strftime('%Y%M%d%H%m%S'),
                         add_etags=False)
    f.seek(0, os.SEEK_END)
    size = f.tell()
    f.seek(0)
    response.headers.extend({
        'Content-Length': size,
        'Cache-Control': 'no-cache'
    })
    
    return response

def _write_all_measurements_csv(outputFile):
    COL_BATCH_CODE = 'BatchId'
    COL_PROCESS_TYPE = 'Process Type'
    COL_ROBOT = 'Robot'
    COL_TEMPERATURE = 'Temperature'
    COL_DATE_PROCESSED = 'DateProcessed'
    COL_UPLOADED_BY = 'Uploaded By'
    COL_PLATE_NAME = 'Plate Name'
    COL_HALF_PLATE = 'Half Plate'
    COL_OPERATOR = 'Operator'
    COL_OPERATOR_CODE = 'Operator Code'
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
    COL_CV = 'CV'
    COL_ERRORLOWT_TO = 'Error Low T_TO'
    COL_ERRORHIGHCV = 'Error High CV'
    COL_ERROR_INVALIDSAMPLECOUNT = 'Error Invalid Sample Count'

    fieldnames = [
        COL_BATCH_CODE,
        COL_PROCESS_TYPE,
        COL_ROBOT,
        COL_TEMPERATURE,
        COL_DATE_PROCESSED,
        COL_UPLOADED_BY,
        COL_PLATE_NAME,
        COL_HALF_PLATE,
        COL_OPERATOR,
        COL_OPERATOR_CODE,
        COL_PRIMER_BATCH,
        COL_ENZYME_BATCH,
        COL_ROTOR_GENE,
        COL_HUMIDITY,
        COL_SAMPLE_CODE,
        COL_ERROR_CODE,
        COL_T_TO,
        COL_T_AMP,
        COL_T,
        COL_S_TO,
        COL_S_AMP,
        COL_S,
        COL_TS,
        COL_CV,
        COL_ERRORLOWT_TO,
        COL_ERRORHIGHCV,
        COL_ERROR_INVALIDSAMPLECOUNT
        ]

    output = csv.DictWriter(outputFile, fieldnames=fieldnames)

    output.writer.writerow(output.fieldnames)

    for measurement in Measurement.query:
        output.writerow({
            COL_BATCH_CODE : measurement.batch.id,
            COL_PROCESS_TYPE : measurement.batch.processType,
            COL_ROBOT : measurement.batch.robot,
            COL_TEMPERATURE : measurement.batch.temperature,
            COL_DATE_PROCESSED : measurement.batch.datetime,
            COL_UPLOADED_BY : measurement.batch.user.username,
            COL_PLATE_NAME : measurement.batch.plateName,
            COL_HALF_PLATE : measurement.batch.halfPlate,
            COL_OPERATOR : measurement.batch.operator.username,
            COL_OPERATOR_CODE : measurement.batch.operator.code,
            COL_PRIMER_BATCH : measurement.batch.primerBatch,
            COL_ENZYME_BATCH : measurement.batch.enzymeBatch,
            COL_ROTOR_GENE : measurement.batch.rotorGene,
            COL_HUMIDITY : measurement.batch.humidity,
            COL_SAMPLE_CODE : measurement.sample.sampleCode,
            COL_ERROR_CODE : measurement.errorCode,
            COL_T_TO : measurement.t_to,
            COL_T_AMP : measurement.t_amp,
            COL_T : measurement.t,
            COL_S_TO : measurement.s_to,
            COL_S_AMP : measurement.s_amp,
            COL_S : measurement.s,
            COL_TS : measurement.ts,
            COL_CV : measurement.coefficientOfVariation,
            COL_ERRORLOWT_TO : measurement.errorLowT_to,
            COL_ERRORHIGHCV : measurement.errorHighCv,
            COL_ERROR_INVALIDSAMPLECOUNT : measurement.errorInvalidSampleCount
            })

def _write_user_errors_csv(outputFile, user_id):
    COL_SAMPLE_CODE = 'Sample Code'
    COL_PLATE_NAME = 'Plate Name'
    COL_WELL = 'Well'
    COL_CONDITION_DESCRIPTION = 'Condition'
    COL_DNA_TEST = 'DNA Test'
    COL_PICO_TEST = 'PICO Test'
    COL_VOLUME = 'Volume'
    COL_ERROR_CODE = 'Error Code'
    COL_ERRORS = 'Other Errors'

    fieldnames = [
        COL_SAMPLE_CODE,
        COL_PLATE_NAME,
        COL_WELL,
        COL_CONDITION_DESCRIPTION,
        COL_DNA_TEST,
        COL_PICO_TEST,
        COL_VOLUME,
        COL_ERROR_CODE,
        COL_ERRORS
        ]

    output = csv.DictWriter(outputFile, fieldnames=fieldnames, quoting=csv.QUOTE_NONNUMERIC)

    output.writer.writerow(output.fieldnames)

    batches_with_errors = Batch.query.filter_by(operatorUserId=user_id).filter(Batch.outstandingErrorCount > 0).all()

    samples_with_errors = Set()

    for b in batches_with_errors:
        for s in Set([m.sample for m in b.measurements if len(m.sample.outstandingErrors) > 0]):

            samplePlate = (s.get_samplePlate_for_plateName(b.plateName) or SamplePlate())

            errorCodes = [m.errorCode for m in b.measurements if m.sample == s]

            maxErrorCode = ''
            if '' not in errorCodes and errorCodes:
                maxErrorCode = max(errorCodes)

            output.writerow({
                COL_SAMPLE_CODE : s.sampleCode,
                COL_PLATE_NAME : b.plateName,
                COL_WELL : samplePlate.well,
                COL_CONDITION_DESCRIPTION : samplePlate.conditionDescription,
                COL_DNA_TEST : samplePlate.dnaTest,
                COL_PICO_TEST : samplePlate.picoTest,
                COL_VOLUME : samplePlate.volume,
                COL_ERROR_CODE : maxErrorCode,
                COL_ERRORS : "; ".join(Set([oe.description for oe in s.outstandingErrors if oe.description[:14] != 'Error code of ' and oe.description[:10] != 'Validated ']))
                })