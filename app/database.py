import os, datetime
from app import db
from flask import g
from contextlib import closing

dbUpgradeDir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'db_upgrade')

print dbUpgradeDir

def init_db() :
    print 'initialising DB'
    db.engine.execute("CREATE TABLE IF NOT EXISTS db_version (id INT AUTO_INCREMENT, version INT, appliedDate DATETIME, PRIMARY KEY(id));")
    currentVersion = db.engine.execute("SELECT MAX(version) maxVersion FROM db_version").fetchall()[0][0] or 0

    print 'Upgrading DB from version %d' % currentVersion

    print 'Upgrade directory is ' + dbUpgradeDir

    upgradeScripts = [f for f in os.listdir(dbUpgradeDir)
                        if f.split('.')[0].isdigit() 
                            and f.split('.')[1] == 'sql' 
                            and os.path.isfile(os.path.join(dbUpgradeDir, f))
                            and int(f.split('.')[0]) > currentVersion]
    
    upgradeScripts.sort(key = lambda s: int(s.split('.')[0]))

    for f in upgradeScripts:
        print 'Running DB script %s' % f

        with open(os.path.join(dbUpgradeDir, f)) as s:
            db.engine.execute(s.read())
            db.engine.execute('INSERT INTO db_version (version, appliedDate) VALUES (%s, %s)', [int(f.split('.')[0]), datetime.datetime.now()])

