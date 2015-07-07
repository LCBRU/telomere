from flask import g, render_template
from flask.ext.login import login_required

from app import telomere
from app.model.user import User

@telomere.route('/')
def index():
    return render_template('index.html')


@telomere.route("/protected/",methods=["GET"])
@login_required
def protected():
    return render_template('protected.html')
