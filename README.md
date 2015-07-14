# Telomere

Record audit information for the telomere length study

## Requirements

    sudo apt-get install libmysqlclient-dev python-dev
    sudo easy_install flask
    sudo easy_install flask-sqlalchemy
    sudo easy_install mysql-python
    sudo easy_install flask-login
    sudo apt-get install libldap2-dev
    sudo apt-get install libsasl2-dev
    sudo pip install python-ldap
    sudo pip install Flask-WTF
    sudo pip WTForms-Components

## Install

1. Copy or clone the source from the git repository.
2. Copy the defaultSettings.py file to settings.py
3. Edit the settings.py file and change the following settings:
	1. Change `Debug` to be false
	2. Change `SECRET_KEY` to a secret key.
	3. Change `DATABASE` to the database name
	4. Change `SQLALCHEMY_DATABASE_URI` to a valid MySQL connection string
	5. Change `LDAP_URL` to be include the server and port for the LDAP service
	6. Change `LDAP_BASEDN` to be a valid one of those things.

## Create the database

The Telomere application creates the tables that it requires,
but first you must create the database and give the user then
necessary permissions.

1. `CREATE DATABASE telomere;`
2. `GRANT ALL PRIVILEGES ON telomere.* to {username}@127.0.0.1 identified by '{password}';`

## Installation on University of Leicester LAMP servers

See [Here](http://lcbru-trac.rcs.le.ac.uk/wiki/Telomere%20Length%20Recording%20Application%20HowTo%20Install).