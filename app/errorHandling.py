from flask import render_template
import logging
import traceback
from app import telomere

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
    telomere.logger.error(traceback.format_exc())
    return render_template('500.html'), 500
