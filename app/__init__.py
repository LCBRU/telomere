import datetime
from flask import Flask, g, render_template
from flask.ext.sqlalchemy import SQLAlchemy
import logging
import traceback

telomere = Flask(__name__)
telomere.config.from_object('app.settings')
telomere.secret_key = telomere.config['SECRET_KEY']

import errorHandling

db = SQLAlchemy(telomere)

import app.database
database.init_db()

@telomere.before_request
def set_date():
    g.year = datetime.datetime.now().year

import app.helpers.templateFilters

from app.views import *
