#!/usr/bin/env python
from app.views.export import write_all_measurements_csv
import tempfile
import os

exportDirectory = "{0}/app/static/exports".format(os.path.dirname(os.path.realpath(__file__)))
workingFile = "{0}/AllMeasurements_inprogress.csv".format(exportDirectory)
finalFile = "{0}/AllMeasurements.csv".format(exportDirectory)

f = open(workingFile, "w")

try:
    write_all_measurements_csv(f)

finally:
    f.close

os.rename(workingFile, finalFile)

