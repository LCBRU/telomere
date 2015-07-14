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

    batch = Batch(
        batchCode = form.batchCode.data,
        robot = form.robot.data,
        pcrMachine = form.pcrMachine.data,
        temperature = form.temperature.data,
        datetime = form.datetime.data,
        userId = current_user.id
        )

    db.session.add(batch)

    return batch

def _saveSampleMeasurements(form, batch):
    for sm in form.samples.entries:
        
        if not sm.sampleCode.data: continue

        sampleId = sm.sampleCode.data

        sample = _getOrCreateSample(sampleId)

        measurement = Measurement(
            batchId=batch.id,
            sampleId=sample.id,
            t1=sm.t1.data,
            s1=sm.s1.data,
            t2=sm.t2.data,
            s2=sm.s2.data,
            tsRatio=sm.tsRatio.data,
            )
        db.session.add(measurement)


def _getOrCreateSample(sampleCode):
    sample = Sample.query.filter_by(sampleCode=sampleCode).first()

    if (not sample):
        sample = Sample(sampleCode=sampleCode)
        db.session.add(sample)
        db.session.flush()
    else:
        flash("Duplicate measurement for sample '%s' recorded." % sampleCode)

    return sample