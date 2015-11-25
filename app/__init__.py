import datetime
from flask import Flask, g
from flask.ext.sqlalchemy import SQLAlchemy
import logging

logging.basicConfig()

telomere = Flask(__name__)
telomere.config.from_object('app.settings')

db = SQLAlchemy(telomere)

import app.database
database.init_db()

telomere.secret_key = telomere.config['SECRET_KEY']

@telomere.before_request
def set_date():
    g.year = datetime.datetime.now().year

import app.helpers.templateFilters

from app.views import *
