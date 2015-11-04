import os, datetime
from werkzeug import secure_filename
from flask_login import current_user
from app import db, telomere
from app.model.manifest import Manifest

class ManifestService():

    def SaveAndReturn(self, manifestFile):
        filename = secure_filename(manifestFile.filename)

        manifest = Manifest(
            filename = filename,
            uploaded = datetime.datetime.now(),
            userId = current_user.id
            )

        db.session.add(manifest)
        db.session.flush()

        manifestFile.save(self.GetPath(manifest))

        return manifest

    def Process(self, manifest):
        errors = []
        samples = self._GetSamplesFromManifest(manifest)

        for sample in samples:
            db.session.add(sample)

        return errors

    def _GetSamplesFromManifest(self, manifest):
        result = []

        wb = load_workbook(filename = self.GetPath(spreadsheet), use_iterators = True)
        ws = wb.get_sheet_by_name(name = 'Sheet1')

        for i in range(1, ws.get_highest_row()):
            sampleCode = ws.cell(column = 0, row = i).value
            volume = ws.cell(column = 1, row = i).value
            concentration = ws.cell(column = 2, row = i).value
            plateId = ws.cell(column = 3, row = i).value

            result.append(Sample(sampleCode = sampleCode, volume = volume, concentration = concentration, plateId = plateId))

        return result

    def GetPath(self, manifest):
        return os.path.join(telomere.config['SPREADSHEET_UPLOAD_DIRECTORY'], self.GetFilename(manifest))

    def GetFilename(self, manifest):
        return "manifest_%d.xlsx" % manifest.id
