from flask import redirect, url_for, request, g, render_template, request
from flask_login import LoginManager, login_user, logout_user, current_user
from app import db
import ldap, time
from urllib.parse import urlparse

from app import telomere
from app.model.user import User

login_manager = LoginManager()
login_manager.init_app(telomere)
login_manager.login_view = "login" 
 
@login_manager.user_loader
def load_user(userId):
    return User.query.filter_by(id=userId).first()
 
@telomere.before_request
def get_current_user():
    g.user = current_user

@telomere.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@telomere.route("/login",methods=["GET", "POST"])
def login():
    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        if validateLDAP(username,password):
            user = User.query.filter_by(username=username).first()
 
            if user:
                login_user(user)
                next = _getValidatedNext()
                return redirect(next or url_for('index'))

        time.sleep(5.5)

    return render_template('user/login.html')

def validateLDAP(username,password):
    ld = ldap.initialize(telomere.config['LDAP_URL'])
    try:
        ld.simple_bind_s(
            'uid={0},{1}'.format(username, telomere.config['LDAP_BASEDN']),
            password
        )
        print("Validated user")
        return True
    except ldap.LDAPError as e:
        print("authentication error")
        print(e)
        return False

def _getValidatedNext():
    o = urlparse(request.url_root)
    q = urlparse(request.args.get('next'))

    if q.hostname is None or q.hostname == o.hostname:
        return request.args.get('next')
