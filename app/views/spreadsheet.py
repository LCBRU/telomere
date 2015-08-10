from flask import flash, redirect, url_for, request, render_template
from flask.ext.login import login_required
from app import db, telomere
from app.forms.spreadsheet import SpreadsheetUpload
from app.services.spreadsheet import SpreadsheetService
from app.model.spreadsheet import Spreadsheet

@telomere.route("/spreadsheet/upload", methods=['GET', 'POST'])
@login_required
def speadsheet_upload():

    form = SpreadsheetUpload()

    if form.validate_on_submit():
        service = SpreadsheetService()
        spreadsheet = service.SaveAndReturn(form.spreadsheet.data)
        service.Process(spreadsheet.id)

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
                per_page=20,
                error_out=False))

@telomere.route("/spreadsheet/process/<int:id>")
@login_required
def speadsheet_process(id):

    return redirect(url_for('speadsheet_index'))
