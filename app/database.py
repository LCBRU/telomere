import os
import datetime
import sys
from app import db, telomere
import traceback

dbUpgradeDir = os.path.join(os.path.abspath(
    os.path.dirname(__file__)), 'db_upgrade')

print(dbUpgradeDir)


def init_db():
    print('initialising DB')
    db.engine.execute('SET sql_notes = 0;')
    db.engine.execute('CREATE TABLE IF NOT EXISTS db_version (id INT AUTO_INCREMENT, version INT, appliedDate DATETIME, PRIMARY KEY(id));')
    db.engine.execute('SET sql_notes = 1;')

    currentVersion = db.engine.execute(
        "SELECT MAX(version) maxVersion FROM db_version").fetchall()[0][0] or 0

    print('Upgrading DB from version {}'.format(currentVersion))

    print('Upgrade directory is ' + dbUpgradeDir)

    upgradeScripts = [f for f in os.listdir(dbUpgradeDir)
                      if f.split('.')[0].isdigit() and
                      f.split('.')[1] == 'sql' and
                      os.path.isfile(os.path.join(dbUpgradeDir, f)) and
                      int(f.split('.')[0]) > currentVersion]

    upgradeScripts.sort(key=lambda s: int(s.split('.')[0]))

    for f in upgradeScripts:
        print('Running DB script {}'.format(f))

        with open(os.path.join(dbUpgradeDir, f)) as s:
            try:
                curUpdate = db.engine.raw_connection().cursor()
                curUpdate.execute(
                    "START TRANSACTION;\n" + s.read() + "\nCOMMIT; ")
                curUpdate.close()

                db.engine.execute(
                    '''INSERT INTO db_version (version, appliedDate)
                        VALUES (%s, %s)''',
                    [int(f.split('.')[0]), datetime.datetime.now()])
            except:
                telomere.logger.error(traceback.format_exc())
                db.engine.raw_connection().cursor().execute("ROLLBACK;")
                print("Unexpected Error: ", sys.exc_info()[0])
                raise
