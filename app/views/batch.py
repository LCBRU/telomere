import datetime
from flask import flash, redirect, url_for, request, g, render_template
from flask_login import login_required
from app import db, telomere
from app.services.batch import BatchService
from app.services.outstandingError import OutstandingErrorService
from app.forms.batch import BatchDelete, BatchEditForm, BatchSearchForm
from app.model.batch import Batch
from app.model.sample import Sample
from app.model.outstandingError import OutstandingError
from app.model.measurement import Measurement
from app.model.user import User
from flask_login import current_user
from app.helpers.wrappers import manifest_required

@telomere.route("/batch/edit/<int:id>", methods=['GET','POST'])
@login_required
@manifest_required
def batch_edit(id):
    batch = Batch.query.get(id)
    form = BatchEditForm(id=id, batch=batch, version_id=batch.version_id)

    users = User.query.order_by(User.code.asc()).all()
    form.batch.operatorUserId.choices = [(u.id, u.GetCodeAndName()) for u in users]

    if form.validate_on_submit():

        if (str(batch.version_id) != str(form.version_id.data)):
            flash("Batch has been updated by another user, please re-enter your changes to the most recent version of the batch.", "error")
            return redirect(url_for('batch_edit', id=id))

        batch.robot = form.batch.robot.data
        batch.temperature = form.batch.temperature.data
        batch.datetime = form.batch.datetime.data
        batch.userId = current_user.id
        batch.plateName = form.batch.plateName.data
        batch.halfPlate = form.batch.halfPlate.data
        batch.humidity = form.batch.humidity.data
        batch.primerBatch = form.batch.primerBatch.data
        batch.enzymeBatch = form.batch.enzymeBatch.data
        batch.rotorGene = form.batch.rotorGene.data
        batch.operatorUserId = form.batch.operatorUserId.data
        batch.batchFailureReason = form.batch.batchFailureReason.data
        batch.processType = form.batch.processType.data

        db.session.commit()
        return redirect(url_for('batch_index'))
            
    return render_template('batch/batchEdit.html', form=form)

@telomere.route('/batch/')
@telomere.route("/batch/<int:page>")
@login_required
@manifest_required
def batch_index(page=1):
    searchString = request.args.get('search')
    form = BatchSearchForm(search=searchString)

    q = Batch.query

    if searchString:
        q = q.filter(Batch.plateName.like("%{0}%".format(searchString)))

    batches = (
        q.order_by(Batch.id.desc())
         .paginate(
            page=page,
            per_page=10,
            error_out=False))

    return render_template('batch/index.html', batches=batches, form=form)


@telomere.route("/batch/delete/<int:id>")
@login_required
def batch_delete(id):
    batch = Batch.query.get(id)
    form = BatchDelete(obj=batch)
    return render_template('batch/delete.html', batch=batch, form=form)

@telomere.route("/batch/delete", methods=['POST'])
@login_required
def batch_delete_confirm():
    form = BatchDelete()

    if form.validate_on_submit():
        batch = Batch.query.get(form.id.data)

        if (batch):
            db.session.delete(batch)
            db.session.commit()
            flash("Deleted batch '%s'." % batch.id)
            
    return redirect(url_for('batch_index'))
