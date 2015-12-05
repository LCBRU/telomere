import datetime
from flask import Flask, g
from flask.ext.sqlalchemy import SQLAlchemy
import logging

    #logging.basicConfig()

telomere = Flask(__name__)
telomere.config.from_object('app.settings')

print telomere.debug
ADMINS = ['rab63@le.ac.uk']
if not telomere.debug:
    print "Hello"
    import logging
    from logging.handlers import SMTPHandler
    mail_handler = SMTPHandler('127.0.0.1',
                               'lcbruit@le.ac.uk',
                               ADMINS, 'Telomere Failed')
    mail_handler.setLevel(logging.ERROR)
    telomere.logger.addHandler(mail_handler)


db = SQLAlchemy(telomere)

import app.database
database.init_db()

telomere.secret_key = telomere.config['SECRET_KEY']

@telomere.before_request
def set_date():
    g.year = datetime.datetime.now().year

@telomere.errorhandler(500)
def internal_error(exception):
    telomere.logger.error(exception)
    return render_template('500.html'), 500

telomere.logger.error("Yellow")

import app.helpers.templateFilters

from app.views import *
