import datetime
from flask import flash, redirect, url_for, request, render_template, send_from_directory
from flask.ext.login import login_required
from app import db, telomere
from app.forms.spreadsheet import SpreadsheetUpload
from app.services.spreadsheet import SpreadsheetService
from app.services.batch import BatchService
from app.model.spreadsheet import Spreadsheet
from app.model.user import User
from app.model.manifest import Manifest
from flask_login import current_user
from app.helpers.wrappers import manifest_required

@telomere.route('/spreadsheet/upload/', methods=['GET', 'POST'])
@login_required
@manifest_required
def speadsheet_upload():

    form = SpreadsheetUpload()

    users = User.query.order_by(User.code.asc()).all()
    form.batch.operatorUserId.choices = [(u.id, u.GetCodeAndName()) for u in users]
    form.batch.operatorUserId.data = current_user.id

    if form.validate_on_submit():

        batchService = BatchService()
        batch = batchService.SaveAndReturn(form.batch)

        if batchService.IsBatchDuplicate(batch):
            if batch.is_initial() or batch.is_replate():
                flash("The plate name and half plate have been used in a previous batch.", "error")
                db.session.rollback()
                return render_template('spreadsheet/upload.html', form=form)
        else:
            if batch.is_duplicate():
                flash("The plate name and half plate have not been used in a previous batch.", "error")
                db.session.rollback()
                return render_template('spreadsheet/upload.html', form=form)

        if (batch and batch.batchFailureReason):
            db.session.commit()
            return redirect(url_for('batch_index'))            

        if (batch):
            spreadsheetService = SpreadsheetService()
            spreadsheet = spreadsheetService.SaveAndReturn(form.spreadsheet.data, batch)

            if not spreadsheetService.ValidateFormat(spreadsheet):
                flash("Spreadsheet does not have a valid format", "error")

                db.session.rollback()
                return render_template('spreadsheet/upload.html', form=form)

            spreadsheetLoadResult = spreadsheetService.Process(spreadsheet, not batch.is_replate())

            if spreadsheetLoadResult.abortUpload():
                if len(spreadsheetLoadResult.missingSampleCodes) > 0:
                    flash("The following samples are not in the manifest: %s" % ", ".join(str(x) for x in spreadsheetLoadResult.missingSampleCodes), "error")
                if len(spreadsheetLoadResult.incorrectPlateName) > 0:
                    flash("The following samples have a different plate name to the manifest: %s" % ", ".join(str(x) for x in spreadsheetLoadResult.incorrectPlateName), "error")

                flash("File '%s' has not been uploaded" % spreadsheet.filename, "error")

                db.session.rollback()
            else:
                flash("File '%s' Uploaded" % spreadsheet.filename)

                if spreadsheetLoadResult.hasOutstandingErrors:
                    flash("Batch was loaded with errors", "warning")

                db.session.commit()

                return redirect(url_for('batch_index'))

    return render_template('spreadsheet/upload.html', form=form)

@telomere.route("/spreadsheet/download/<int:id>")
@login_required
def speadsheet_download(id):
    spreadsheet = Spreadsheet.query.get(id)
    service = SpreadsheetService()

    return send_from_directory(telomere.config['SPREADSHEET_UPLOAD_DIRECTORY'], service.GetFilename(spreadsheet), as_attachment=True, attachment_filename=spreadsheet.filename)


