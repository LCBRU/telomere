import datetime
from flask import flash, redirect, url_for, request, render_template
from flask.ext.login import login_required
from werkzeug import secure_filename
from app import db, telomere
from flask_login import current_user
from app.forms.spreadsheet import SpreadsheetUpload
from app.model.spreadsheet import Spreadsheet

@telomere.route("/spreadsheet/upload", methods=['GET', 'POST'])
@login_required
def speadsheet_upload():

    form = SpreadsheetUpload()

    if form.validate_on_submit():
        filename = secure_filename(form.spreadsheet.data.filename)

        spreadsheet = Spreadsheet(
            filename = filename,
            uploaded = datetime.datetime.now(),
            userId = current_user.id
            )

        db.session.add(spreadsheet)
        db.session.commit()

    #        form.spreadsheet.data.save('uploads/' + filename)
        flash("File '%s' Uploaded" % filename)
        return redirect(url_for('index'))

    return render_template('spreadsheet/upload.html', form=form)
