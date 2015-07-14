import datetime
from flask import flash, redirect, url_for, request, g, render_template
from flask.ext.login import login_required
from app import db, telomere
from app.forms.batch import BatchEntry
from app.model.batch import Batch
from app.model.sample import Sample
from flask_login import current_user

@telomere.route("/batch/entry", methods=['GET', 'POST'])
@login_required
def batch_entry():
    item = Batch()
    item.datetime = datetime.datetime.now()
    form = BatchEntry(obj=item, operator=current_user.username)

    if form.validate_on_submit():
        batch = _saveBatch(form)

        if (batch):
            _saveSampleMeasurements(form, batch)

            db.session.commit()
            return redirect(url_for('index'))

    return render_template('batch/batchEntry.html', form=form)

def _saveBatch(form):
    batch = Batch.query.filter_by(batchId=form.batchId.data).first()

    if (batch):
        flash("Batch ID already exists", "error")
        return False

    batch = Batch()
    batch.batchId = form.batchId.data
    batch.robot = form.robot.data
    batch.pcrMachine = form.pcrMachine.data
    batch.temperature = form.temperature.data
    batch.datetime = form.datetime.data
    batch.userId = current_user.id
    db.session.add(batch)

    return batch

def _saveSampleMeasurements(form, batch):
    for formSample in form.samples.entries:
        sample = _saveSample(formSample)

def _saveSample(formSample):
    sampleId = formSample.sampleId.data

    if (sampleId):
        sample = Sample.query.filter_by(sampleId=sampleId).first()

        if (not sample):
            sample = Sample(sampleId=sampleId)
            db.session.add(sample)
        else:
            flash("Duplicate measurement for sample '%s' recorded." % sampleId)

        return sample