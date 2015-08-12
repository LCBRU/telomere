import datetime
from flask import flash, redirect, url_for, request, g, render_template
from flask.ext.login import login_required
from app import db, telomere
from app.services.batch import BatchService
from app.forms.batch import BatchAndSampleForm
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
            return redirect(url_for('index'))

    return render_template('batch/batchEntry.html', form=form)

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