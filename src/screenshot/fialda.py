import http.cookiejar as cookielib
from seleniumUtils import *
import sys
import os 
import datetime
import shutil
import numpy
from dotenv import load_dotenv
load_dotenv(dotenv_path='stock.env')
import logging
import logging.config
logging.config.fileConfig(fname='log.conf', disable_existing_loggers=False)
logger = logging.getLogger()
import pandas as pd
from sendScreenshot import send

#Constants
HEAD_LESS= True # True: won't display the browser and vice versa
#Variables
#--------------------------#
failedSymbols = []
timeframe = ""
symbols = None
dateRange = ""
path = ""
def parseCookieFile(cookiefile):
    cj = cookielib.MozillaCookieJar(cookiefile)
    cj.load()
    cookies =[]
    for c in cj:
        cookies.append({"name":c.name, "value": c.value, "domain": c.domain})
    return cookies

def shoot(textTimeFrame, symbols, location, isMerged):
    try:
        inputArgs = sys.argv
        # textTimeFrame = timeframe.lower().replace("_"," ")
        path = location
        # Create folder
        if os.path.isdir(path) and isMerged:
            print("[Directory already exist:]", path)
            shutil.rmtree(path, ignore_errors=True)
            os.mkdir(path) 

        withChrome(HEAD_LESS)
        url = "https://fialda.com/phan-tich-ky-thuat"
        cookies = parseCookieFile('cookies.txt')
        gotoURL(url, cookies)
        # Close popup video
        myClick("//span[@class='ant-modal-close-x']")
        # Change theme
        myClick("//i[@class='ico-darkmode']")
        # Goto iframe
        switchToIframe("//iframe[contains(@id,'tradingview')]")
        
        # Change timeframe
        myClick("//div[@id='header-toolbar-intervals']")
        myClick("//div[contains(@class,'menuWrap')]//div[contains(text(),'" + textTimeFrame +"')]")
        #INCREASE FONT SIZE to 14
        myClick("//div[@id='header-toolbar-properties']")
        # myClick("//div[@data-name='series-properties-dialog']")
        myClick("//div[@data-name='appearance']")
        myClick("//div[@data-name='font-size-select']")
        myClick("//div[@data-name='menu-inner']/div/div/div[text()='14']")
        myClick("//button[@name='submit']")
        # OPEN RSI & MOMENTUM INDICATORS
        myClick("//div[@id='header-toolbar-indicators']")
        mySendKey("//div[@data-dialog-name='Indicators']/div/div/input", "Momentum")
        myClick("//span[@title='Momentum']")
        mySendKey("//div[@data-dialog-name='Indicators']/div/div/input", "Stochastic")
        myClick("//span[@title='Stochastic']")
        mySendKey("//div[@data-dialog-name='Indicators']/div/div/input", "Bollinger Bands")
        myClick("//span[@title='Bollinger Bands']")
        myClick("//span[@data-name='close']")

        # FORMAT INDICATOR
        # MOMENTUM
        myHoverAndClick("//div[@data-name='legend-source-title'][text()='Mom']")
        myClick("//div[@data-name='legend-source-title'][text()='Mom']/../..//div[@data-name='legend-settings-action']")
        myClick("//div[@data-dialog-name='Mom']//div[text()='Inputs']")
        mySendKey("//div[@data-dialog-name='Mom']//input[@value='10']", "12")

        myClick("//div[@data-dialog-name='Mom']//div[text()='Style']")
        myClick("//div[@data-name='color-with-thickness-select']")
        myClick("//div[contains(@class,'swatches')]//div[@style='color: rgb(0, 0, 0);']")
        myClick("//div[@data-dialog-name='Mom']//div[text()='Style']")
        myClick("//button[@name='submit']")


        for symbol in symbols:
            try:
                mySendKey("//div[@id='header-toolbar-symbol-search']/div/input", symbol)
                press(Keys.DOWN)
                press(Keys.RETURN)
                pause(1)
                # Full screen
                # myClick("//div[@class='group-wWM3zP_M-'][10]")
                # SCREEN SHOT
                screenShot("{}{}_{}.png".format(path, symbol, textTimeFrame))
                # exit fullscreen
                # press(Keys.ESCAPE)
            except:
                    failedSymbols.append(symbol)
                    traceback.print_exc()
        logger.info("Screenshot Fialda successfully")
    except Exception as e:
        logger.error("Failed to screenshot {} {}".format(textTimeFrame, location))
        logger.error(e)
        traceback.print_exc()
    finally:
        quit()
    if len(failedSymbols) > 0:
        logger.info("Failed symbols" + failedSymbols)
        numpyArray = numpy.asarray(failedSymbols)
        numpy.savetxt(path + "/fialda_missing.csv", numpyArray, delimiter=",")

def getStocks(stockFile):
    return list(pd.read_csv(stockFile, header=None)[0])

if __name__ == '__main__':
    if (sys.argv[1] == 'daily'):
        shoot("1 day", getStocks(os.getenv('all_stocks')), os.getenv('screenshot_1day'), True)
    elif (sys.argv[1] == 'weekly'):
        shoot("1 week", getStocks(os.getenv('all_stocks')), os.getenv('screenshot_1week'), True)
    elif (sys.argv[1] == 'monthly'):
        shoot("1 month", getStocks(os.getenv('all_stocks')), os.getenv('screenshot_1month'), True)
    elif (sys.argv[1] == '15m'):
        shoot("15 minutes", getStocks(os.getenv('following_stocks')) + getStocks(os.getenv('portfolio')), os.getenv('screenshot_15min'), True)
        if (len(sys.argv) == 3):
            send("15 minutes", os.getenv('screenshot_15min'))
    elif (sys.argv[1] == '1h'):
        shoot("1 hour", getStocks(os.getenv('following_stocks')) + getStocks(os.getenv('portfolio')), os.getenv('screenshot_1h'), True)
        if (len(sys.argv) == 3):
            send("1 hour", os.getenv('screenshot_1h'))
    elif (sys.argv[1] == '1d'):
        shoot("1 day", getStocks(os.getenv('following_stocks')) + getStocks(os.getenv('portfolio')), os.getenv('screenshot_realtime_1day'), True)
        if (len(sys.argv) == 3):
            send("1 day", os.getenv('screenshot_realtime_1day'))
    else:
        if (sys.argv[1] == 'portfolio'):
            stocks = getStocks(os.getenv('portfolio'))
            location = os.getenv('screenshot_portfolio')
            print("Portfolio")
        elif (sys.argv[1] == 'following'):
            stocks = getStocks(os.getenv('following_stocks'))
            location = os.getenv('screenshot_following')
            print("Following")
        elif (sys.argv[1] == 'vn30'):
            stocks = getStocks(os.getenv('vn30'))
            location = os.getenv('screenshot_vn30')
            print("VN30")
        else:
            print("List of stocks")
            stocks = sys.argv[1].split(",")
            location = os.getenv('screenshot_urgent')
        shoot("1 day", stocks, location, True)
        shoot("15 minutes", stocks, location, False)
        shoot("1 hour", stocks, location, False)
        if (len(sys.argv) == 3):
            send(sys.argv[1], location)