import os, datetime
from werkzeug import secure_filename
from flask_login import current_user
from app import db, telomere
from app.model.manifest import Manifest
from app.model.sample import Sample
from openpyxl import load_workbook

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

        wb = load_workbook(filename = self.GetPath(manifest), use_iterators = True)
        ws = wb.get_sheet_by_name(name = 'Sheet1')

        for row in ws.iter_rows(row_offset=1):
            result.append(Sample(
                sampleCode = row[0].value,
                volume = row[1].value,
                concentration = row[2].value,
                plateId = row[3].value))

        return result

    def GetPath(self, manifest):
        return os.path.join(telomere.config['SPREADSHEET_UPLOAD_DIRECTORY'], self.GetFilename(manifest))

    def GetFilename(self, manifest):
        return "manifest_%d.xlsx" % manifest.id
