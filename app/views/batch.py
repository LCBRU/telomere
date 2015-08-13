import datetime
from flask import flash, redirect, url_for, request, g, render_template
from flask.ext.login import login_required
from app import db, telomere
from app.services.batch import BatchService
from app.services.sample import SampleService
from app.forms.batch import BatchAndSampleForm, BatchDelete
from app.model.batch import Batch
from app.model.sample import Sample
from app.model.measurement import Measurement
from flask_login import current_user

@telomere.route("/batch/entry", methods=['GET', 'POST'])
@login_required
def batch_entry():
    form = BatchAndSampleForm(batch = {'operator': current_user.username, 'datetime': datetime.datetime.now()})

    if form.validate_on_submit():
        batchService = BatchService()
        batch = batchService.SaveAndReturn(form.batch)

        if (batch):
            _saveSampleMeasurements(form, batch)

            db.session.commit()
            return redirect(url_for('batch_index'))

    return render_template('batch/batchEntry.html', form=form)

def _saveSampleMeasurements(form, batch):
    for sm in form.samples.entries:
        
        if not sm.sampleCode.data: continue

        sampleId = sm.sampleCode.data

        sampleService = SampleService()
        sample = sampleService.GetOrCreateSample(sampleId)

        measurement = Measurement(
            batchId=batch.id,
            sampleId=sample.id,
            t1=sm.t1.data,
            s1=sm.s1.data,
            t2=sm.t2.data,
            s2=sm.s2.data,
            )
        db.session.add(measurement)

@telomere.route('/batch/')
@telomere.route("/batch/page:<int:page>")
@login_required
def batch_index(page=1):

    return render_template('batch/index.html', batches=Batch.query
            .order_by(Batch.datetime.desc())
            .paginate(
                page=page,
                per_page=10,
                error_out=False))


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
            flash("Deleted batch '%s'." % batch.batchCode)
            
    return redirect(url_for('batch_index'))
