import datetime
from flask import flash, redirect, url_for, request, render_template, send_from_directory
from flask.ext.login import login_required
from app import db, telomere
from app.model.manifest import Manifest
from app.forms.manifest import ManifestUpload
from app.services.manifest import ManifestService
from flask_login import current_user

@telomere.route('/manifest/')
@telomere.route("/manifest/page:<int:page>")
@login_required
def manifest_index(page=1):

    manifest_count = Manifest.query.count()

    if manifest_count == 0:
        return redirect(url_for('manifest_upload'))

    manifests = (Manifest
        .query
        .order_by(Manifest.uploaded.desc())
        .paginate(
            page=page,
            per_page=10,
            error_out=False))

    return render_template('manifest/index.html', manifests=manifests)

@login_required
@telomere.route('/manifest/upload/', methods=['GET', 'POST'])
def manifest_upload():

    form = ManifestUpload(manifest = {'uploaded': datetime.datetime.now()})

    if form.validate_on_submit():
        manifestService = ManifestService()
        manifest = manifestService.SaveAndReturn(form.manifest.data)
        errors = manifestService.Process(manifest)

        if len(errors) > 0:
            flash("The following samples have already been loaded in a previous manifest: %s" % ", ".join(str(x) for x in errors), "error")

            db.session.rollback()
        else:
            flash("File '%s' Uploaded" % manifest.filename)

            db.session.commit()

            return redirect(url_for('manifest_index'))

    return render_template('manifest/upload.html', form=form)

@telomere.route("/manifest/download/<int:id>")
@login_required
def manifest_download(id):
    manifest = Manifest.query.get(id)
    service = ManifestService()

    return send_from_directory(telomere.config['SPREADSHEET_UPLOAD_DIRECTORY'], service.GetFilename(manifest), as_attachment=True, attachment_filename=manifest.filename)
