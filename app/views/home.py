from flask import g
from flask.ext.login import login_required

from app import telomere
from app.model.user import User

@telomere.route('/')
def index():
    return 'Even Newer Home'


@telomere.route("/protected/",methods=["GET"])
@login_required
def protected():
    return "Hello %s!" % g.user.username
 
