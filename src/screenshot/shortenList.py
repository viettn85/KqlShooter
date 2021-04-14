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

reports = 'results/'

def captureDay(trend):
    pictures = list(filter(lambda x: os.path.splitext(x)
                           [1], os.listdir(reports + trend)))
    symbols = list(map(lambda x: x[0:3], pictures))
    today = datetime.today().strftime("%Y-%m-%d")
    capture("day", today, trend, "-".join(symbols))
    # df = pd.read_csv(report, index_col="Date")
    # print(df.head())
    # columns = df.columns
    # # columns = ["PinBar1"]
    # row = df.iloc[0]
    # if date != "":
    #     try:
    #         row = df.iloc[df.index.get_loc(str(date))]
    #     except:
    #         print("The input date {} of {} is not existed".format(date, report))
    #         sys.exit(1)
    # else:
    #     date = df.index.values[0]
    # for col in columns:
    #     if not (type(row[col]) == float):
    #         capture(duration, date, col, row[col])

if __name__ == '__main__':
    captureDay(sys.argv[1])