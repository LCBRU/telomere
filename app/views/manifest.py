import datetime
from flask import flash, redirect, url_for, request, render_template, send_from_directory
from flask_login import login_required
from app import db, telomere
from app.model.manifest import Manifest
from app.forms.manifest import ManifestUpload, ManifestDelete
from app.services.manifest import ManifestService
from flask_login import current_user
from app.helpers.wrappers import manifest_required

@telomere.route('/manifest/')
@telomere.route("/manifest/page:<int:page>")
@login_required
@manifest_required
def manifest_index(page=1):

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

        if not manifestService.ValidateFormat(manifest):
            flash("Manifest spreadsheet does not have a valid format", "error")
            db.session.rollback()

        else:
            db.session.flush()
            
            if not manifestService.Process(manifest):
                flash("Manifest has not been uploaded because it contained duplicate samples or other errors", "error")

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

@telomere.route("/manifest/delete/<int:id>")
@login_required
def manifest_delete(id):
    manifest = Manifest.query.get(id)
    form = ManifestDelete(obj=manifest)
    return render_template('manifest/delete.html', manifest=manifest, form=form)

@telomere.route("/manifest/delete", methods=['POST'])
@login_required
def manifest_delete_confirm():
    form = ManifestDelete()

    if form.validate_on_submit():
        manifest = Manifest.query.get(form.id.data)

        if (manifest):
            db.session.delete(manifest)
            db.session.commit()
            flash("Deleted manifest '%s'." % manifest.filename)
            
    return redirect(url_for('manifest_index'))

