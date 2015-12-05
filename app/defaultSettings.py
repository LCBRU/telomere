# configuration
DEBUG = True
SECRET_KEY = 'secretkey'

# Uploads
SPREADSHEET_UPLOAD_DIRECTORY = '/upload/path/'

# Database
DATABASE = 'databasename'
SQLALCHEMY_DATABASE_URI = 'connection_string'
SQLALCHEMY_ECHO = True

# LDAP
LDAP_URL = 'ldaps://ldap_server:port'
LDAP_BASEDN = 'base_dn'

# Emailing
SMTP_SERVER = '127.0.0.1'
ADMIN_EMAIL_ADDRESSES = ['bob@example.com']
APPLICATION_EMAIL_ADDRESSES = 'telomere@example.com'
ERROR_EMAIL_SUBJECT = 'Telomere Failed'