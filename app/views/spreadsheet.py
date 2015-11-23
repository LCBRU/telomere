import datetime
from flask import flash, redirect, url_for, request, render_template, send_from_directory
from flask.ext.login import login_required
from app import db, telomere
from app.forms.spreadsheet import SpreadsheetUpload
from app.services.spreadsheet import SpreadsheetService
from app.services.batch import BatchService
from app.model.spreadsheet import Spreadsheet
from app.model.user import User
from flask_login import current_user

@login_required
@telomere.route('/spreadsheet/upload/', methods=['GET', 'POST'])
def speadsheet_upload():

    form = SpreadsheetUpload()

    users = User.query.order_by(User.code.asc()).all()
    form.batch.operatorUserId.choices = [(u.id, u.GetCodeAndName()) for u in users]
    form.batch.operatorUserId.data = current_user.id

    if form.validate_on_submit():
        batchService = BatchService()
        batch = batchService.SaveAndReturn(form.batch)

        if (batch and batch.failed):
            db.session.commit()

            return redirect(url_for('batch_index'))
            

        if (batch):
            spreadsheetService = SpreadsheetService()
            spreadsheet = spreadsheetService.SaveAndReturn(form.spreadsheet.data, batch)
            spreadsheetLoadResult = spreadsheetService.Process(spreadsheet)

            if spreadsheetLoadResult.abortUpload():
                if len(spreadsheetLoadResult.missingSampleCodes) > 0:
                    flash("The following samples are not in the manifest: %s" % ", ".join(str(x) for x in spreadsheetLoadResult.missingSampleCodes), "error")

                if len(spreadsheetLoadResult.plateMismatchCodes) > 0:
                    flash("The following samples are for a different plate: %s" % ", ".join(str(x) for x in spreadsheetLoadResult.plateMismatchCodes), "error")

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


