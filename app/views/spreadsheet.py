import datetime
from flask import flash, redirect, url_for, request, render_template, send_from_directory
from flask.ext.login import login_required
from app import db, telomere
from app.forms.spreadsheet import SpreadsheetUpload
from app.services.spreadsheet import SpreadsheetService
from app.services.batch import BatchService
from app.model.spreadsheet import Spreadsheet
from flask_login import current_user

@login_required
@telomere.route('/spreadsheet/upload/', methods=['GET', 'POST'])
def speadsheet_upload():

    form = SpreadsheetUpload(batch = {'operator': current_user.username, 'datetime': datetime.datetime.now()})

    if form.validate_on_submit():
        batchService = BatchService()
        batch = batchService.SaveAndReturn(form.batch)

        if (batch):
            spreadsheetService = SpreadsheetService()
            spreadsheet = spreadsheetService.SaveAndReturn(form.spreadsheet.data, batch)
            spreadsheetService.Process(spreadsheet)

            flash("File '%s' Uploaded" % spreadsheet.filename)

            return redirect(url_for('speadsheet_index'))

    return render_template('spreadsheet/upload.html', form=form)

@telomere.route('/spreadsheet/')
@telomere.route("/spreadsheet/page:<int:page>")
@login_required
def speadsheet_index(page=1):

    return render_template('spreadsheet/index.html', spreadsheets=Spreadsheet.query
            .order_by(Spreadsheet.uploaded.desc())
            .paginate(
                page=page,
                per_page=10,
                error_out=False))

@telomere.route("/spreadsheet/process/<int:id>", methods=['POST'])
@login_required
def speadsheet_process(id):

    return redirect(url_for('speadsheet_index'))

@telomere.route("/spreadsheet/details/<int:id>")
@login_required
def speadsheet_details(id):
    service = SpreadsheetService()
    return render_template('spreadsheet/details.html', details=service.GetDetails(id))

@telomere.route("/spreadsheet/download/<int:id>")
@login_required
def speadsheet_download(id):
    spreadsheet = Spreadsheet.query.get(id)
    service = SpreadsheetService()

    return send_from_directory(telomere.config['SPREADSHEET_UPLOAD_DIRECTORY'], service.GetFilename(spreadsheet), as_attachment=True, attachment_filename=spreadsheet.filename)
