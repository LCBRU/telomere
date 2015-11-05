import os, datetime
from werkzeug import secure_filename
from flask_login import current_user
from app import db, telomere
from app.model.spreadsheet import Spreadsheet
from app.model.measurement import Measurement, MeasurementSet
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
        errors = []
        measurementSets = self._GetMeasurementSetsFromSpreadsheet(spreadsheet)

        for sampleCode, ms in measurementSets.iteritems():
            if len(ms) != 2:
                errors.append("Sample %s has %d set(s) of measurement instead of 2" % (sampleCode, len(ms)) )

        if len(errors) == 0:
            for sampleCode, ms in measurementSets.iteritems():
                sample = Sample.query.filter_by(sampleCode=sampleCode).first()

                measurement = Measurement(
                    batchId=spreadsheet.batch.id,
                    sampleId=sample.id,
                    t1=ms[0].tValue,
                    s1=ms[0].sValue,
                    t2=ms[1].tValue,
                    s2=ms[1].sValue,
                    )
                db.session.add(measurement)

        return errors

    def _GetMeasurementSetsFromSpreadsheet(self, spreadsheet):
        result = {}

        wb = load_workbook(filename = self.GetPath(spreadsheet), use_iterators = True)
        ws = wb.get_sheet_by_name(name = 'Sheet1')

        for i in range(1, ws.get_highest_row()):
            sampleCode = ws.cell(column = 24, row = i).value
            tValue = ws.cell(column = 25, row = i).value
            sValue = ws.cell(column = 26, row = i).value

            if (sampleCode is not None and str(sampleCode).isdigit()):
                measurementSets = []

                if (result.has_key(sampleCode)):
                    measurementSets = result[sampleCode]

                else:
                    result[sampleCode] = measurementSets

                measurementSets.append(MeasurementSet(tValue, sValue))

        return result


    def GetPath(self, spreadsheet):
        return os.path.join(telomere.config['SPREADSHEET_UPLOAD_DIRECTORY'], self.GetFilename(spreadsheet))

    def GetFilename(self, spreadsheet):
        return "%d.xlsx" % spreadsheet.id
