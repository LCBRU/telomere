import os, datetime
from sets import Set
from werkzeug import secure_filename
from flask_login import current_user
from app import db, telomere
from app.model.manifest import Manifest
from app.model.sample import Sample
from openpyxl import load_workbook
import traceback
from decimal import *

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
        wb = load_workbook(filename = self.GetPath(manifest), use_iterators = True)
        ws = wb.worksheets[0]

        try:
            chunks = [iter(ws.iter_rows(row_offset=1))] * 10

            for c in chunks[1:2]:
#                for row in c:
#                    print row[2].value

#                db.engine.execute(
#                    Sample.__table__.insert(),
#                    [{  "plateName": row[0].value,
#                        "well": row[1].value,
#                        "sampleCode": row[2].value,
#                        "conditionDescription": row[3].value,
#                        "volume": row[4].value,
#                       "dnaTest": row[5].value,
#                        "picoTest": row[6].value,
#                        "manifestId": manifest.id}
#                        for row in c if len(row[2].value) > 0])

                db.session.bulk_insert_mappings(
                    Sample,
                    [{  "plateName": row[0].value,
                        "well": row[1].value,
                        "sampleCode": row[2].value,
                        "conditionDescription": row[3].value,
                        "volume": row[4].value,
                        "dnaTest": Decimal(Decimal(row[5].value).quantize(Decimal('.01'), rounding=ROUND_HALF_UP)),
                        "picoTest": Decimal(Decimal(row[6].value).quantize(Decimal('.01'), rounding=ROUND_HALF_UP)),
                        "manifestId": manifest.id}
                        for row in c]
                    )
        except:
            telomere.logger.error(traceback.format_exc())
            return False

        return True

    def ValidateFormat(self, manifest):

        wb = load_workbook(filename = self.GetPath(manifest), use_iterators = True)
        ws = wb.worksheets[0]

        return (
            ws['A1'].value == 'Plate Name' and
            ws['B1'].value == 'WELL' and
            ws['C1'].value == 'Sample_Name' and
            ws['D1'].value == 'Condition' and
            ws['E1'].value == 'Volume' and
            ws['F1'].value == 'DNA Test (ng/ul)' and
            ws['G1'].value == 'Pico Test (ng/ul)')

    def GetPath(self, manifest):
        return os.path.join(telomere.config['SPREADSHEET_UPLOAD_DIRECTORY'], self.GetFilename(manifest))

    def GetFilename(self, manifest):
        return "manifest_%d.xlsx" % manifest.id
