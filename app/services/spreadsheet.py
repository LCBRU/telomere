import os, datetime
from werkzeug import secure_filename
from flask_login import current_user
from app import db, telomere
from app.model.spreadsheet import Spreadsheet

class SpreadsheetService():

    def SaveAndReturn(self, spreadsheetFile):
        filename = secure_filename(spreadsheetFile.filename)

        spreadsheet = Spreadsheet(
            filename = filename,
            uploaded = datetime.datetime.now(),
            userId = current_user.id
            )

        db.session.add(spreadsheet)
        db.session.commit()

        spreadsheetFile.save(self._GetPath(spreadsheet))

        return spreadsheet

    def Process(self, spreadsheetId):
    	return 1

    def _GetPath(self, spreadsheet):
        return os.path.join(telomere.config['SPREADSHEET_UPLOAD_DIRECTORY'], "%d.xls" % spreadsheet.id)