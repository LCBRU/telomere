import datetime
from flask import redirect, url_for, request, g, render_template
from flask.ext.login import login_required
from app import db, telomere
from app.forms.batch import BatchEntry
from app.model.batch import Batch
from flask_login import current_user

@telomere.route("/batch/entry", methods=['GET', 'POST'])
@login_required
def batch_entry():
    item = Batch()
    item.datetime = datetime.datetime.now()
    form = BatchEntry(obj=item, operator=current_user.username)
    if form.validate_on_submit():
        item.batchId = form.batchId.data
        item.robot = form.robot.data
        item.pcrMachine = form.pcrMachine.data
        item.temperature = form.temperature.data
        item.datetime = form.datetime.data
        item.userId = current_user.id
        db.session.add(item)
        db.session.commit()
        print item.id
        return redirect(url_for('index'))

    return render_template('batch/batchEntry.html', form=form)