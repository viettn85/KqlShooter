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
import traceback

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

def shoot(textTimeFrame, symbols, location):
    try:
        inputArgs = sys.argv
        # textTimeFrame = timeframe.lower().replace("_"," ")
        path = location
        # Create folder
        if os.path.isdir(path):
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
        myClick("//div[@class='_tv-dialog-content']")
        myClick("//div[@class='_tv-dialog-content']/div/a[3]")
        myClick("//div[@class='tv-select-container dialog tv-select-container-fontsize']/a[@class='sbToggle']")
        myClick("//div[@class='tv-select-container dialog tv-select-container-fontsize sbHolderOpen']/ul[@class='sbOptions']/li/a[@rel='14']")
        myClick("//a[@class='_tv-button ok']")
        # OPEN RSI & MOMENTUM INDICATORS
        myClick("//div[@id='header-toolbar-indicators']")
        myClick("//div[@class='tv-insert-study-item__title-text' and text()='Momentum']")
        myClick("//div[@class='tv-insert-study-item__title-text' and contains(string(), 'Stochastic')]")
        myClick("//div[@class='tv-insert-study-item__title-text' and contains(string(), 'Bollinger Band')]")
        myClick("//div[@class='tv-insert-study-item__title-text' and contains(string(), 'Relative Strength')]")
        myClick("//div[@class='tv-dialog__close js-dialog__close']")

        # FORMAT INDICATOR
        # MOMENTUM
        myClick("//div[@class='pane-legend-line pane-legend-wrap study']/span[contains(text(),'Mom')]/../span[@class='pane-legend-icon-container']/a[@class='pane-legend-icon apply-common-tooltip format']")
        myClick("//div[@class='_tv-dialog-content']")
        myClick("//div[@class='tv-ticker__btn tv-ticker__btn--up']", 2)

        # myClick("//div[@class='_tv-dialog-content']")
        # myClick("//input[@class='ticker tv-text-input inset dialog']/../../../../../../div[@class='properties-tabs tv-tabs ui-draggable-handle']/a[2]")
        # myClick("//span[@class='tvcolorpicker-container']")
        # myClick("//div[@style='background-color: rgb(0, 0, 0);']")

        # myClick("//div[@class='_tv-dialog-content']")
        # myClick("//div[@class='linewidth-slider ui-slider ui-corner-all ui-slider-horizontal ui-widget ui-widget-content']")
        myClick("//a[@class='_tv-button ok']")
        # changeStyle("//span[@class='ui-slider-handle ui-corner-all ui-state-default']", 'left', 100)

        # Stoch
        # myClick("//div[@class='pane-legend-line pane-legend-wrap study']/span[contains(text(),'Stoch')]/../span[@class='pane-legend-icon-container']/a[@class='pane-legend-icon apply-common-tooltip format']")
        # myClick("//div[@class='_tv-dialog-content']")
        # myClick("//input[@class='ticker tv-text-input inset dialog']/../../../../../../div[@class='properties-tabs tv-tabs ui-draggable-handle']/a[1]")
        # myClick("//td[contains(text(),'length')]/../td//div[@class='tv-ticker__btn tv-ticker__btn--up']", 7)
        # myClick("//td[contains(text(),'smoothK')]/../td//div[@class='tv-ticker__btn tv-ticker__btn--up']", 6)
        # myClick("//td[contains(text(),'smoothD')]/../td//div[@class='tv-ticker__btn tv-ticker__btn--up']", 4)
        # myClick("//a[@class='_tv-button ok']")

        # RSI
        # myClick("//div[@class='pane-legend-line pane-legend-wrap study']/span[contains(text(),'Bol')]/../span[@class='pane-legend-icon-container']/a[@class='pane-legend-icon apply-common-tooltip format']")
        # myClick("//div[@class='_tv-dialog-content']")
        # myClick("//a[@class='_tv-button ok']")

        for symbol in symbols:
            try:
                mySendKey("//div[@id='header-toolbar-symbol-search']/div/input", symbol)
                press(Keys.DOWN)
                press(Keys.RETURN)
                # Full screen
                myClick("//div[@class='group-wWM3zP_M-'][10]")
                # SCREEN SHOT
                screenShot("{}{}_{}.png".format(path, symbol, textTimeFrame))
                # exit fullscreen
                press(Keys.ESCAPE)
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
    # return ['BID']

if __name__ == '__main__':
    if (sys.argv[1] == 'daily'):
        shoot("1 day", getStocks(os.getenv('all_stocks')), os.getenv('screenshot_1day'))
    if (sys.argv[1] == 'weekly'):
        shoot("1 week", getStocks(os.getenv('all_stocks')), os.getenv('screenshot_1week'))
    if (sys.argv[1] == 'monthly'):
        shoot("1 month", getStocks(os.getenv('all_stocks')), os.getenv('screenshot_1month'))
    if (sys.argv[1] == '15m'):
        shoot("15 minutes", getStocks(os.getenv('following_stocks')) + getStocks(os.getenv('portfolio')), os.getenv('screenshot_15min'))
        if (len(sys.argv) == 3):
            send("15 minutes", os.getenv('screenshot_15min'))
    if (sys.argv[1] == '1h'):
        shoot("1 hour", getStocks(os.getenv('following_stocks')) + getStocks(os.getenv('portfolio')), os.getenv('screenshot_1h'))
        if (len(sys.argv) == 3):
            send("1 hour", os.getenv('screenshot_1h'))
    if (sys.argv[1] == '1d'):
        shoot("1 day", getStocks(os.getenv('following_stocks')) + getStocks(os.getenv('portfolio')), os.getenv('screenshot_realtime_1day'))
        if (len(sys.argv) == 3):
            send("1 day", os.getenv('screenshot_realtime_1day'))
