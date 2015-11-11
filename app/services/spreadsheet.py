import os, datetime, re
from sets import Set
from werkzeug import secure_filename
from flask_login import current_user
from app import db, telomere
from app.model.spreadsheet import Spreadsheet
from app.model.measurement import Measurement
from app.model.sample import Sample
from app.model.outstandingError import OutstandingError
from openpyxl import load_workbook

class SpreadsheetService():

    def SaveAndReturn(self, spreadsheetFile, batch):
        filename = secure_filename(spreadsheetFile.filename)

        spreadsheet = Spreadsheet(
            filename = filename,
            uploaded = datetime.datetime.now(),
            userId = current_user.id,
            batchId = batch.id
            )

        db.session.add(spreadsheet)
        db.session.flush()

        spreadsheetFile.save(self.GetPath(spreadsheet))

        return spreadsheet

    def Process(self, spreadsheet):
        result = SpreadsheetLoadResult()

        wb = load_workbook(filename = self.GetPath(spreadsheet), use_iterators = True)
        ws = wb.worksheets[0]

        for row in ws.iter_rows(row_offset=1):

            sampleCode = row[23].value #Col X

            if (sampleCode is None or not str(sampleCode).isdigit()):
                continue

            sample = Sample.query.filter_by(sampleCode=sampleCode).first()

            if sample is None:
                result.missingSampleCodes.add(sampleCode)
                continue

            if sample.plateName != spreadsheet.batch.plateName:
                result.plateMismatchCodes.add(sampleCode)
                continue

            measurement = Measurement(
                batchId=spreadsheet.batch.id,
                sampleId=sample.id,
                t_to=row[1].value, #Col B
                t_amp=row[2].value, #Col C
                t=row[3].value, #Col D
                s_to=row[13].value, #Col N
                s_amp=row[14].value, #Col O
                s=row[15].value, #Col P
                errorCode=row[29].value or '' #Col AD
                )
            db.session.add(measurement)

            if (measurement.HasErrors()):
                outstandingError = OutstandingError(
                    description = measurement.GetErrorDescription(),
                    batchId = spreadsheet.batch.id,
                    sampleId = sample.id
                    )

                db.session.add(outstandingError)
                result.hasOutstandingErrors = True

        return result

    def GetPath(self, spreadsheet):
        return os.path.join(telomere.config['SPREADSHEET_UPLOAD_DIRECTORY'], self.GetFilename(spreadsheet))

    def GetFilename(self, spreadsheet):
        return "%d.xlsx" % spreadsheet.id

    def _isValidValue(self, value):
        valAsString = str(value)
        p = re.compile('\d+(\.\d+)?')
        return p.match(valAsString) != None

class SpreadsheetLoadResult:

    def __init__(self, *args, **kwargs):
        self.missingSampleCodes = Set()
        self.plateMismatchCodes = Set()
        self.hasOutstandingErrors = False

    def abortUpload(self):
        return len(self.missingSampleCodes) > 0 or len(self.plateMismatchCodes) > 0