import datetime
from flask import flash, redirect, url_for, request, g, render_template
from flask.ext.login import login_required
from app import db, telomere
from app.forms.batch import BatchEntry
from app.model.batch import Batch
from app.model.sample import Sample
from app.model.measurement import Measurement
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
    batch = Batch.query.filter_by(batchCode=form.batchCode.data).first()

    if (batch):
        flash("Batch Code already exists", "error")
        return False

    batch = Batch()
    batch.batchCode = form.batchCode.data
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

        if (sample):
            measurement = Measurement(
                batchId=batch.id,
                sampleId=sample.id,
                t1=formSample.t1.data,
                s1=formSample.s1.data,
                t2=formSample.t2.data,
                s2=formSample.s2.data,
                tsRatio=formSample.tsRatio.data,
                )
            db.session.add(measurement)


def _saveSample(formSample):
    sampleCode = formSample.sampleCode.data

    if (sampleCode):
        sample = Sample.query.filter_by(sampleCode=sampleCode).first()

        if (not sample):
            sample = Sample()
            sample.sampleCode = sampleCode
            db.session.add(sample)
            db.session.flush()
        else:
            flash("Duplicate measurement for sample '%s' recorded." % sampleCode)

        return sample