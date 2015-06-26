from flask import Flask, redirect, url_for, request, g
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager, UserMixin, login_required, login_user, current_user
import ldap

import defaultSettings

telomere = Flask(__name__)
telomere.config.from_object('app.settings')

db = SQLAlchemy(telomere)

import app.database
database.init_db()

from app.model.user import User

login_manager = LoginManager()
login_manager.init_app(telomere)
login_manager.login_view = "login_here" 
 
@login_manager.user_loader
def load_user(userId):
    return User.query.filter_by(id=userId).first()
 
@telomere.before_request
def get_current_user():
    g.user = current_user

@telomere.route("/login_here",methods=["GET", "POST"])
def login_here():
    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        if validateLDAP(username,password):
            user = User.query.filter_by(username=username).first()
 
            if not user:
                user = User(username)
                db.session.add(user)
                db.session.commit()

            login_user(user)
            return redirect(url_for('index'))

    return '''
        <form action="" method="post">
            <label for=username>Username</label><input type=text name=username>
            <label for=password>Password</label><input type=password name=password>
            <input type=submit value=Login>
        </form>
    '''

def validateLDAP(username,password):
    ld = ldap.initialize(telomere.config['LDAP_URL'])
    try:
        ld.simple_bind_s(
            'uid={0},{1}'.format(username, telomere.config['LDAP_BASEDN']),
            password
        )
        print "Validated user"
        return True
    except ldap.LDAPError, e:
        print "authentication error"
        print e
        return False

@telomere.route("/protected/",methods=["GET"])
@login_required
def protected():
    return "Hello %s!" % g.user.username
 
from app import views

