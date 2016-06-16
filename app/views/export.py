from flask import g, send_file, render_template, redirect, url_for
from flask.ext.login import login_required
import tempfile, os, csv, datetime
from flask_login import current_user
from sets import Set
from sqlalchemy.orm import joinedload
from sqlalchemy.sql import text
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
        write_all_measurements_csv(f)

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

def write_all_measurements_csv(outputFile):
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

    cmd = """
        SELECT
              b.id AS batchId
            , b.processType
            , b.robot
            , b.temperature
            , b.datetime
            , u.username
            , b.plateName
            , b.halfPlate
            , o.username AS operator_name
            , o.code AS operator_code
            , b.primerBatch
            , b.enzymeBatch
            , b.rotorGene
            , b.humidity
            , s.sampleCode
            , m.errorCode
            , m.t_to
            , m.t_amp
            , m.t
            , m.s_to
            , m.s_amp
            , m.s
            , m.ts
            , m.coefficientOfVariation
            , m.errorLowT_to
            , m.errorHighCv
            , m.errorInvalidSampleCount
        FROM    measurement m
        JOIN    batch b ON b.id = m.batchId
        JOIN    sample s ON s.id = m.sampleId
        JOIN    user u ON u.id = b.userId
        JOIN    user o ON o.id = b.operatorUserId
        ;
    """

    measurements = db.engine.execute(text(cmd))
    for m in measurements:
        output.writerow({
            COL_BATCH_CODE : m[0],
            COL_PROCESS_TYPE : m[1],
            COL_ROBOT : m[2],
            COL_TEMPERATURE : m[3],
            COL_DATE_PROCESSED : m[4],
            COL_UPLOADED_BY : m[5],
            COL_PLATE_NAME : m[6],
            COL_HALF_PLATE : m[7],
            COL_OPERATOR : m[8],
            COL_OPERATOR_CODE : m[9],
            COL_PRIMER_BATCH : m[10],
            COL_ENZYME_BATCH : m[11],
            COL_ROTOR_GENE : m[12],
            COL_HUMIDITY : m[13],
            COL_SAMPLE_CODE : m[14],
            COL_ERROR_CODE : m[15],
            COL_T_TO : m[16],
            COL_T_AMP : m[17],
            COL_T : m[18],
            COL_S_TO : m[19],
            COL_S_AMP : m[20],
            COL_S : m[21],
            COL_TS : m[22],
            COL_CV : m[23],
            COL_ERRORLOWT_TO : m[24],
            COL_ERRORHIGHCV : m[25],
            COL_ERROR_INVALIDSAMPLECOUNT : m[26]
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

    cmd = """
    SELECT
          s.sampleCode
        , b.plateName
        , sp.well
        , sp.conditionDescription
        , sp.dnaTest
        , sp.picoTest
        , sp.volume
        , MAX(m.errorCode) AS errorCode
        , GROUP_CONCAT(DISTINCT oe.description SEPARATOR '; ') AS errors
    FROM    measurement m
    JOIN    outstandingError oe ON  oe.sampleId = m.sampleId
                                AND oe.batchId = m.batchId
    JOIN    sample s ON s.id = m.sampleId
    JOIN    batch b ON b.id = m.batchId
    LEFT JOIN   samplePlate sp ON   sp.sampleCode = s.sampleCode
                                AND sp.plateName = b.plateName
    WHERE   oe.description NOT LIKE 'Validated %'
        AND b.operatorUserId = :userId
    GROUP BY
          s.sampleCode
        , b.plateName
        , sp.well
        , sp.conditionDescription
        , sp.dnaTest
        , sp.picoTest
        , sp.volume
    ;
    """

    measurements = db.engine.execute(text(cmd), userId = user_id)
    for m in measurements:
        output.writerow({
            COL_SAMPLE_CODE : m[0],
            COL_PLATE_NAME : m[1],
            COL_WELL : m[2],
            COL_CONDITION_DESCRIPTION : m[3],
            COL_DNA_TEST : m[4],
            COL_PICO_TEST : m[5],
            COL_VOLUME : m[6],
            COL_ERROR_CODE : m[7],
            COL_ERRORS : m[8]
        })
