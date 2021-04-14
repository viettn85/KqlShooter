from shutil import copyfile
import pandas as pd
import sys

duration = "W-2020-10-26"
# duration = "W-2020-11-02"

def copyScreenshots(trend):
    df = pd.read_csv("results/{}.csv".format(trend))
    for stock in df.Stock:
        copyfile("results/{}/{}/{}.png".format(duration, trend, stock), "results/{}/{}.png".format(trend, stock))

if __name__ == '__main__':
    copyScreenshots(sys.argv[1])