from flask import Flask, session, redirect, url_for, escape, request
from flask.ext.login import login_required, login_user, logout_user

from app import telomere

@telomere.route('/')
def index():
    if 'username' in session:
        return 'Logged in as %s' % escape(session['username'])
    return 'You are not logged in'

@telomere.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return '''
        <form action="" method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''

@telomere.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
    

# set the secret key.  keep this really secret:
telomere.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'


