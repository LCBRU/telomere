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
        spreadsheetSamples = self._GetSpreadsheetSamples(spreadsheet)

        for sampleCode, ss in spreadsheetSamples.iteritems():
            if len(ss.measurementSets) != 2:
                errors.append("Sample %s has %d set(s) of measurement instead of 2" % (sampleCode, len(ms)) )

            if ss.sample is None:
                errors.append("Sample %s does not exist in the manifest" % (sampleCode))

        if len(errors) == 0:
            for sampleCode, ss in spreadsheetSamples.iteritems():
                measurement = Measurement(
                    batchId=spreadsheet.batch.id,
                    sampleId=ss.sample.id,
                    t1=ss.measurementSets[0].tValue,
                    s1=ss.measurementSets[0].sValue,
                    t2=ss.measurementSets[1].tValue,
                    s2=ss.measurementSets[1].sValue,
                    )
                db.session.add(measurement)

        return errors

    def _GetSpreadsheetSamples(self, spreadsheet):
        result = {}

        wb = load_workbook(filename = self.GetPath(spreadsheet), use_iterators = True)
        ws = wb.get_sheet_by_name(name = 'Sheet1')

        for row in ws.iter_rows(row_offset=1):
            sampleCode = row[23].value
            tValue = row[24].value
            sValue = row[25].value

            if (sampleCode is not None and str(sampleCode).isdigit()):

                if (result.has_key(sampleCode)):
                    spreadsheetSample = result[sampleCode]

                else:
                    sample = Sample.query.filter_by(sampleCode=sampleCode).first()
                    spreadsheetSample = SpreadsheetSample(sampleCode = sampleCode, sample = sample)
                    result[sampleCode] = spreadsheetSample

                spreadsheetSample.measurementSets.append(MeasurementSet(tValue, sValue))

        return result


    def GetPath(self, spreadsheet):
        return os.path.join(telomere.config['SPREADSHEET_UPLOAD_DIRECTORY'], self.GetFilename(spreadsheet))

    def GetFilename(self, spreadsheet):
        return "%d.xlsx" % spreadsheet.id

class SpreadsheetSample():

    def __init__(self, sampleCode, sample):
        self.sampleCode = sampleCode
        self.sample = sample
        self.measurementSets = []