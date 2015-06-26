from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

telomere = Flask(__name__)
telomere.config.from_object('app.settings')

db = SQLAlchemy(telomere)

import app.database
database.init_db()

telomere.secret_key = telomere.config['SECRET_KEY']

from app.views import *
