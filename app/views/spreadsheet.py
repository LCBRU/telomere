import datetime
from flask import flash, redirect, url_for, request, render_template
from flask.ext.login import login_required
from werkzeug import secure_filename
from app import db, telomere
from flask_login import current_user

@telomere.route("/spreadsheet/upload", methods=['GET', 'POST'])
@login_required
def speadsheet_upload():

    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            flash("File '%s' Uploaded" % filename)
            return redirect(url_for('index'))

    return render_template('spreadsheet/upload.html')
