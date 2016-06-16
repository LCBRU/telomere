#!/usr/bin/env python
from app.views.export import write_all_measurements_csv
import tempfile

f = open("app/static/exports/AllMeasurements.csv", "w")

try:
    write_all_measurements_csv(f)

finally:
    f.close

