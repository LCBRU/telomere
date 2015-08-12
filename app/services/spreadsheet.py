import os, datetime
from werkzeug import secure_filename
from flask_login import current_user
from app import db, telomere
from app.model.spreadsheet import Spreadsheet
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
        db.session.commit()

        spreadsheetFile.save(self.GetPath(spreadsheet))

        return spreadsheet

    def Process(self, spreadsheetId):
    	return 1

    def GetPath(self, spreadsheet):
        return os.path.join(telomere.config['SPREADSHEET_UPLOAD_DIRECTORY'], self.GetFilename(spreadsheet))

    def GetFilename(self, spreadsheet):
        return "%d.xlsx" % spreadsheet.id

    def GetDetails(self, spreadsheetId):
        path = os.path.join(telomere.config['SPREADSHEET_UPLOAD_DIRECTORY'], "%d.xlsx" % spreadsheetId)

        result = ""

        wb = load_workbook(filename = path, use_iterators = True)
        ws = wb.get_sheet_by_name(name = 'Sheet1')

        for i in range(1, ws.get_highest_row()):
            sampleId = ws.cell(column = 24, row = i).value
            tValue = ws.cell(column = 25, row = i).value
            sValue = ws.cell(column = 26, row = i).value

            if (sampleId is not None and str(sampleId).isdigit()):
                result += "Sample ID: %s; T = %s; S = %s\n" % (sampleId, tValue, sValue)

        return result

