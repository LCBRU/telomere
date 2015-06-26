from flask import Flask, redirect, url_for, request
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager, UserMixin, login_required, login_user

import defaultSettings

telomere = Flask(__name__)
telomere.config.from_object('app.defaultSettings')

db = SQLAlchemy(telomere)

import app.database
database.init_db()

from app.model.user import User

login_manager = LoginManager()
login_manager.init_app(telomere)
login_manager.login_view = "login_here" 
 
class User(UserMixin):
    # proxy for a database of users
    user_database = {"JohnDoe": ("JohnDoe", "John"),
               "JaneDoe": ("JaneDoe", "Jane")}
 
    def __init__(self, username, password):
        self.id = username
        self.password = password
 
    @classmethod
    def get(cls,id):
        userData = cls.user_database.get(id)
        return User(userData[0], userData[1])
 
 
@login_manager.user_loader
def load_user(userId):
    print "User ID is: "
    print userId
    return User.get(userId)
 
@telomere.route("/login_here",methods=["GET", "POST"])
def login_here():
    if request.method == 'POST':
        username = request.form['username']
        user = User.get(username)

        if user is not None:
            login_user(user)

        return redirect(url_for('index'))
    return '''
        <form action="" method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''

@telomere.route("/protected/",methods=["GET"])
@login_required
def protected():
    return "Hello Protected World!"
 
from app import views

