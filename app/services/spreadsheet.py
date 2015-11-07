import os, datetime
from sets import Set
from werkzeug import secure_filename
from flask_login import current_user
from app import db, telomere
from app.model.spreadsheet import Spreadsheet
from app.model.measurement import Measurement
from app.model.sample import Sample
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
        missingSampleCodes = Set()

        wb = load_workbook(filename = self.GetPath(spreadsheet), use_iterators = True)
        ws = wb.worksheets[0]

        for row in ws.iter_rows(row_offset=1):
            sampleCode = row[23].value #Col X
            errorCode = row[29].value or '' #Col AD

            if (sampleCode is None or not str(sampleCode).isdigit()):
                continue #This is not a row that we are looking for - it's blank or a header or suttin

            sample = Sample.query.filter_by(sampleCode=sampleCode).first()

            if sample is None:
                missingSampleCodes.add(sampleCode)

            if len(missingSampleCodes) == 0:
                measurement = Measurement(
                    batchId=spreadsheet.batch.id,
                    sampleId=sample.id,
                    t_to=row[1].value, #Col B
                    t_amp=row[2].value, #Col C
                    t=row[3].value, #Col D
                    s_to=row[13].value, #Col N
                    s_amp=row[14].value, #Col 0
                    s=row[15].value, #Col P
                    ts=row[26].value, #Col AA
                    errorCode=errorCode
                    )
                db.session.add(measurement)

        return missingSampleCodes

    def GetPath(self, spreadsheet):
        return os.path.join(telomere.config['SPREADSHEET_UPLOAD_DIRECTORY'], self.GetFilename(spreadsheet))

    def GetFilename(self, spreadsheet):
        return "%d.xlsx" % spreadsheet.id