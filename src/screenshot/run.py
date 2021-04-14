from dotenv import load_dotenv
import pandas as pd
import logging
import logging.config
import trendet
import os
from datetime import datetime
from dateutil.parser import parse
import sys
from vnd import capture

reports = 'reports/'

def screenshot(duration, report, date=""):
    df = pd.read_csv(report, index_col="Date")
    print(df.head())
    columns = df.columns
    # columns = ["PinBar1"]
    row = df.iloc[0]
    if date != "":
        try:
            row = df.iloc[df.index.get_loc(str(date))]
        except:
            print("The input date {} of {} is not existed".format(date, report))
            sys.exit(1)
    else:
        date = df.index.values[0]
    for col in columns:
        if not (type(row[col]) == float):
            capture(duration, date, col, row[col])

if __name__ == '__main__':
    if sys.argv[1] == "week":
        reportFile = "weekTrends.csv"
    if sys.argv[1] == "day":
        reportFile = "dayTrends.csv"
    if len(sys.argv) == 2:
        screenshot(sys.argv[1], reports + reportFile)
    if len(sys.argv) == 3:
        screenshot(sys.argv[1], reports + reportFile, sys.argv[2])