import datetime
from flask import flash, redirect, url_for, request, g, render_template
from flask.ext.login import login_required
from app import db, telomere
from app.services.batch import BatchService
from app.forms.batch import BatchDelete, BatchEditForm, BatchCompleteAllErrors, BatchCompleteError
from app.model.batch import Batch
from app.model.sample import Sample
from app.model.outstandingError import OutstandingError
from app.model.measurement import Measurement
from app.model.user import User
from flask_login import current_user

@telomere.route("/batch/edit/<int:id>", methods=['GET','POST'])
@login_required
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
        batch.pcrMachine = form.batch.pcrMachine.data
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

        db.session.commit()
        return redirect(url_for('batch_index'))
            
    return render_template('batch/batchEdit.html', form=form)

@telomere.route('/batch/')
@telomere.route('/batch/<errorsOnly>')
@telomere.route("/batch/page/<int:page>")
@telomere.route("/batch/<errorsOnly>/page/<int:page>")
@login_required
def batch_index(page=1, errorsOnly=None):

    batchQuery = Batch.query

    if errorsOnly is not None and len(errorsOnly) > 0:
        batchQuery = Batch.query.filter(Batch.outstandingErrorCount > 0)

    batches = (batchQuery
        .order_by(Batch.id.desc())
        .paginate(
            page=page,
            per_page=10,
            error_out=False))

    return render_template('batch/index.html', batches=batches, errorsOnly=errorsOnly)


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

@telomere.route("/batch/<int:id>/errors/")
@telomere.route("/batch/<int:id>/errors/<int:page>")
@login_required
def batch_errors(id, page=1):
    batch = Batch.query.get(id)
    errors = (OutstandingError
                .query
                .filter_by(batchId=id)
                .join(OutstandingError.sample)
                .order_by(Sample.sampleCode)
                .paginate(
                    page=page,
                    per_page=10,
                    error_out=False))

    completeAllForm = BatchCompleteAllErrors(obj=batch)
    completeErrorForm = BatchCompleteError()

    return render_template('batch/errors.html', batch=batch, outstandingErrors=errors, completeAllForm=completeAllForm, completeErrorForm=completeErrorForm)

@telomere.route("/batch/errors/complete/", methods=['POST'])
@login_required
def batch_error_complete_post():
    form = BatchCompleteError()

    if form.validate_on_submit():
        batchService = BatchService()

        oe = OutstandingError.query.get(form.id.data)
        batchService.CompleteError(oe)

        db.session.commit()
        flash("Error completed")

        return redirect(url_for('batch_errors', id=form.batchId.data, page=form.page.data))
    else:
        flash("Something went wrong", "error")

    return redirect(url_for('batch_index'))



@telomere.route("/batch/errors/complete_all", methods=['POST'])
@login_required
def batch_errors_complete_all():
    form = BatchCompleteAllErrors()

    if form.validate_on_submit():
        batchService = BatchService()

        batch = Batch.query.get(form.id.data)
        batchService.CompleteAllErrors(batch)

        db.session.commit()
        flash("All error completed")
    else:
        flash("Something went wrong", "error")

    return redirect(url_for('batch_index'))

