import datetime
from flask import Flask, g, render_template
from flask.ext.sqlalchemy import SQLAlchemy
import logging
import traceback

telomere = Flask(__name__)
telomere.config.from_object('app.settings')
telomere.secret_key = telomere.config['SECRET_KEY']

if not telomere.debug:
    import logging
    from logging.handlers import SMTPHandler
    mail_handler = SMTPHandler(telomere.config['SMTP_SERVER'],
                               telomere.config['APPLICATION_EMAIL_ADDRESSES'],
                               telomere.config['ADMIN_EMAIL_ADDRESSES'],
                               telomere.config['ERROR_EMAIL_SUBJECT'])
    mail_handler.setLevel(logging.ERROR)
    telomere.logger.addHandler(mail_handler)

@telomere.errorhandler(500)
@telomere.errorhandler(Exception)
def internal_error(exception):
    print(traceback.format_exc())
    telomere.logger.error(traceback.format_exc())
    return render_template('500.html'), 500

db = SQLAlchemy(telomere)

import app.database
database.init_db()

@telomere.before_request
def set_date():
    g.year = datetime.datetime.now().year

import app.helpers.templateFilters

from app.views import *
