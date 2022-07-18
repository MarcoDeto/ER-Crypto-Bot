from datetime import datetime
import numpy as np

from config import ICHIMOKU_PARAMS

dataArray = np.array([0])
ichimokuStatus = False
current_low = 0
current_high = 0

class Ichimoku:
    def __init__(self, symbol, api, params, interval):
        self.symbol = symbol
        self.api = api
        self.params = params
        self.interval = interval
        self.dataArray = np.array([0])
        self.ichimokuStatus = False
        self.current_high = 0.0
        self.current_low = 0.0


def get_neccesaries(datalist):
    returndata = []
    for window in datalist:
        returndata.append(list(map(float, window[2:4])))
    return np.array(returndata)


def setInitialData (data):
    global dataArray, ichimokuStatus, current_low, current_high
    dataArray = get_neccesaries(data)
    ichimokuStatus = False
    tenkan_sen = ((dataArray[:,0][-ICHIMOKU_PARAMS[0]:].max()) + (dataArray[:,1][-ICHIMOKU_PARAMS[0]:].min()))/2
    kijun_sen = ((dataArray[:,0][-ICHIMOKU_PARAMS[1]:].max()) + (dataArray[:,1][-ICHIMOKU_PARAMS[1]:].min()))/2
    senkou_span_A = (tenkan_sen + kijun_sen) / 2
    senkou_span_B = ((dataArray[:,0][-ICHIMOKU_PARAMS[2]:].max()) + (dataArray[:,1][-ICHIMOKU_PARAMS[2]:].min()))/2
    
    current_high = dataArray[:,0][-1]
    current_low = dataArray[:,1][-1]
    print("initialized with current high " + str(current_high) + " low " + str(current_low))
    
    if(senkou_span_A > senkou_span_B):
        ichimokuStatus = True
    else:
        ichimokuStatus = False
    
    return ichimokuStatus


def calculateChange(currentPrice, symbol, interval):
    global dataArray, ichimokuStatus, current_low, current_high

    if (currentPrice > current_high):
        current_high = currentPrice
        calculate_ichimoku(symbol, interval)
    if (currentPrice < current_low):
        current_low = currentPrice
        calculate_ichimoku(symbol, interval)


def calculate_ichimoku(symbol, interval):
    global dataArray, ichimokuStatus, current_low, current_high
    currentDataArray = dataArray.copy()
    highs = np.append(currentDataArray[:, 0][:-1], current_high).copy()
    lows = np.append(currentDataArray[:, 1][:-1], current_low).copy()
    tenkan_sen = (float(highs[-ICHIMOKU_PARAMS[0]:].max()) + float(lows[-ICHIMOKU_PARAMS[0]:].min())) / 2
    kijun_sen = (float(highs[-ICHIMOKU_PARAMS[1]:].max()) + float(lows[-ICHIMOKU_PARAMS[1]:].min())) / 2
    senkou_span_A = float(tenkan_sen + kijun_sen) / 2
    senkou_span_B = (float(highs[-ICHIMOKU_PARAMS[2]:].max()) + float(lows[-ICHIMOKU_PARAMS[2]:].min())) / 2
    #print ("Symbol   " + self.symbol + "   A: " + str(senkou_span_A) + " B: " + str(senkou_span_B) )

    if(ichimokuStatus == True and (senkou_span_A < senkou_span_B) and len(dataArray) >= max(ICHIMOKU_PARAMS)):
        print("alert " + symbol + " from true to false in interval " + interval  + " where A : "  + str(senkou_span_A) + " B : " + str(senkou_span_B) +"   Time   "+ str(datetime.now()))
        ichimokuStatus = False

    if(ichimokuStatus == False and (senkou_span_A >= senkou_span_B) and len(dataArray) >= max(ICHIMOKU_PARAMS)):
        ichimokuStatus = True
        print("alert " + symbol + " from false to true in interval " + interval + " where Senkou Span A : "  + str(senkou_span_A) + "Senkou Span B : " + str(senkou_span_B) + "  Time   "+ str(datetime.now()))
        # sym = symbol
        # if(self.api == "bittrex"):
        #     index = self.symbol.find('-')
        #     sym = self.symbol[index + 1:] + self.symbol[:index]
        # interv = ""
        # if interval == 'h':
        #     interv = "1H"
        # elif interval == 'q':
        #     interv = "4H"
        # elif interval == 'D':
        #     interv = "D"
        # ex = "BINANCE" if self.api == "binance" else "BITTREX"
        # DiscordMessager.sendMessage("Alert in " + sym + " in exchanghe " + ex + " in interval " +interv+" The tradingview link = https://www.tradingview.com/chart/?symbol=" + ex +":"+sym +"\n Screenshot link and Ichimoku URL to be sent soon.")
        # links = screenShotGenerator.get_trading_view_graph(interval=self.interval, currency=sym,exchange=ex)
        # DiscordMessager.sendMessage("Screenshot: " + links[0] + "   TradingView with Ichimoku link: " + links[1])

