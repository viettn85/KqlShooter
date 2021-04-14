import pandas as pd
from seleniumUtils import *
import urllib.request
import sys
import os 
import datetime
import schedule
import time

intraday = 'data/market/intraday/'
def capture(duration, path, symbols):
    failedSymbols = []
    for symbol in symbols:
        try:
            dateRange = ""
            timeframe = duration

            if timeframe.lower() == "month".lower():
                timeframe = "M"
                dateRange = 'unlimit'
                # path = "./results/" + "Month-" + datetime.datetime.now().strftime('%Y-%m-%d')
            elif timeframe.lower() == "week".lower():
                timeframe = "W"
                # path = "./results/" + "Week-" + datetime.datetime.now().strftime('%Y-%m-%d')
            elif timeframe.lower() == "day".lower():
                timeframe = "D"
                # path = "./results/" + "Day-" + datetime.datetime.now().strftime('%Y-%m-%d')

            # if timeframe.lower() == "week".lower():
            #     timeframe = "W"
            #     dateRange = '1y'
            # elif timeframe.lower() == "day".lower():
            #     timeframe = "D"
            #     dateRange = "3p"
            # elif timeframe.lower() == "month".lower():
            #     timeframe = "M"
            try:
                os.remove(path + "/" + symbol + "-" + timeframe + ".png")
            except:
                print("")
            withChrome(True) # True: don't display the browser and vice versa
            # print("Screenshot {}".format(symbol))
            # gotoURL("https://dchart.vndirect.com.vn/?language=vi&symbol=" +symbol+ "&timeframe=" +timeframe)

            url = "https://dchart.vndirect.com.vn/?language=vi&symbol=" +symbol+ "&timeframe="
            if dateRange == "unlimit":
                url = url +  "W&from=1054568659&to=1093275858"
            else:
                url = url + timeframe
            gotoURL(url)
            print("Screenshoting {}".format(symbol))
            switchToIframe("//iframe[contains(@id,'tradingview')]")      
            # myClick("//div[@class='apply-common-tooltip' and contains(string(), '" +  dateRange +"')]")

            if dateRange == "unlimit":
                pause(0.3) # Wait to load all history data. It's base on your network
                myClick("//div[@id='header-toolbar-intervals']")
                myClick("//div[@class='label-3Xqxy756-' and contains(string(), '1 tháng')]")
            
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
            myClick("//div[@class='tv-dialog__close js-dialog__close']")

            # FORMAT INDICATOR
            # MOMENTUM
            myClick("//div[@class='pane-legend-line pane-legend-wrap study']/span[contains(text(),'Mom')]/../span[@class='pane-legend-icon-container']/a[@class='pane-legend-icon apply-common-tooltip format']")
            myClick("//div[@class='_tv-dialog-content']")
            myClick("//div[@class='tv-ticker__btn tv-ticker__btn--up']", 4)

            myClick("//div[@class='_tv-dialog-content']")
            myClick("//input[@class='ticker tv-text-input inset dialog']/../../../../../../div[@class='properties-tabs tv-tabs ui-draggable-handle']/a[2]")
            myClick("//span[@class='tvcolorpicker-container']")
            myClick("//div[@style='background-color: rgb(0, 0, 0);']")

            myClick("//div[@class='_tv-dialog-content']")
            myClick("//div[@class='linewidth-slider ui-slider ui-corner-all ui-slider-horizontal ui-widget ui-widget-content']")
            myClick("//a[@class='_tv-button ok']")
            # changeStyle("//span[@class='ui-slider-handle ui-corner-all ui-state-default']", 'left', 100)

            # RSI
            myClick("//div[@class='pane-legend-line pane-legend-wrap study']/span[contains(text(),'Stoch')]/../span[@class='pane-legend-icon-container']/a[@class='pane-legend-icon apply-common-tooltip format']")
            myClick("//div[@class='_tv-dialog-content']")
            myClick("//input[@class='ticker tv-text-input inset dialog']/../../../../../../div[@class='properties-tabs tv-tabs ui-draggable-handle']/a[1]")
            myClick("//td[contains(text(),'chiều dài')]/../td//div[@class='tv-ticker__btn tv-ticker__btn--up']", 7)
            myClick("//td[contains(text(),'smoothK')]/../td//div[@class='tv-ticker__btn tv-ticker__btn--up']", 6)
            myClick("//td[contains(text(),'smoothD')]/../td//div[@class='tv-ticker__btn tv-ticker__btn--up']", 4)
            myClick("//a[@class='_tv-button ok']")
            

            # Take screenshot
            myClick("//div[@class='group-wWM3zP_M-'][9]") 
            waitUntilExist("//a[contains(@class,'link')]")
            url = myGetAttrFromXPath("//a[contains(@class,'link')]", 'href')
            urllib.request.urlretrieve(url, path + "/" + symbol + "-" + timeframe + ".png")

        except:
            traceback.print_exc()
            # failedSymbols.append(symbol)
            print("Failed to capture {}".format(symbol))
        finally:
            quit()
    df = pd.DataFrame.from_dict({"Stock": failedSymbols})
    df.to_csv(path + "/missing.csv")

def createFolders(timeframe, date, trend):
    path = "results/{}-{}".format(timeframe, date)
    if not os.path.isdir(path):
        os.mkdir(path) 
    path = "results/{}-{}/{}".format(timeframe, date, trend)
    if not os.path.isdir(path):
        os.mkdir(path) 
    return path

def dailyScreenshot(path):
    df = pd.read_csv(path + ".csv", header=None)
    capture("day", path, list(df[0]))

def highvolScreenshot(path):
    df = pd.read_csv(path + ".csv", header=None)
    capture("day", "screenshots/highvol", list(df[0])[1:])
    # print(list(df[0])[1:])

def hotShot():
    dailyScreenshot("screenshots/portfolio")
    dailyScreenshot("screenshots/following")

def dailyShot():
    dailyScreenshot("screenshots/portfolio")
    dailyScreenshot("screenshots/following")
    dailyScreenshot("screenshots/vn30")

if __name__ == '__main__':
    if len(sys.argv) == 1:
        dailyScreenshot("screenshots/portfolio")
        dailyScreenshot("screenshots/following")
        dailyScreenshot("screenshots/vn30")
    else:
        if sys.argv[1] == "portfolio":
            dailyScreenshot("screenshots/portfolio")
        if sys.argv[1] == "following":
            dailyScreenshot("screenshots/following")
        if sys.argv[1] == "auto":
            schedule.every().day.at("11:30").do(hotShot)
            schedule.every().day.at("12:30").do(hotShot)
            schedule.every().day.at("15:00").do(hotShot)
            schedule.every().day.at("16:00").do(dailyShot)
            while True:
                schedule.run_pending()
                time.sleep(1)
        if sys.argv[1] == "vn30":
            dailyScreenshot("screenshots/vn30")
        if sys.argv[1] == "daily":
            dailyShot()
