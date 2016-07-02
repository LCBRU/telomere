#!/usr/bin/env python
from app.views.export import write_all_measurements_csv
import tempfile
import os

f = open("{0}/app/static/exports/AllMeasurements_inprogress.csv".format(os.path.dirname(os.path.realpath(__file__))), "w")

try:
    write_all_measurements_csv(f)

finally:
    f.close

os.rename("app/static/exports/AllMeasurements_inprogress.csv", "app/static/exports/AllMeasurements.csv")

