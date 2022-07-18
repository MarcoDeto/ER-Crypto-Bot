import time
from tkinter import N
from apiConnection import *
from models.ichimoku import *

hour1,hour4,day1 = {},{},{}
symbols = ['BTCUSDT', 'ETHUSDT']

def __main__():
    global hour1,hour4,day1, symbols
    timeDifference = getTimeDifference()
    
    print("Making initial API call with ichimoku params " + str(ICHIMOKU_PARAMS))
    (hour1,hour4,day1) = initialize(symbols)
    print("Getting Kline Data")
    onehourdata = getData('h', symbols)
    fourhourdata = getData('q', symbols)
    onedaydata = getData('d', symbols)
    print("Distributing initial data to calculator nodes")
    distribute_hourly_data(datadict=onehourdata)
    distribute_fourhour_data(datadict=fourhourdata)
    distribute_daily_data(datadict=onedaydata)
    print("Entering Loop")
    timeStamp = (getTime() - timeDifference)
    detect1h = int(timeStamp // 3600)
    detect4h = int(timeStamp // 14400)
    detect1d = int(timeStamp // 86400)
    while True:
        #get new klines after 10 seconds the server time update, to be sure
        delay = int(getTime() - 10000 - timeDifference)
        difference1d = (delay // 86400)
        difference4h = (delay // 14400)
        difference1h = (delay // 3600)

        if(difference1d != detect1d):
            detect1d = difference1d
            onedaydata = getData('d', symbols)
            distribute_daily_data(datadict=onedaydata)
            print("renew daily")

        elif(difference4h != detect4h):
            detect4h = difference4h
            distribute_fourhour_data(datadict=fourhourdata)
            print("renew quarterly")

        elif (difference1h != detect1h):
            detect1h = difference1h
            onehourdata = getData('h', symbols)
            distribute_hourly_data(datadict=onehourdata)
            print("renew hourly")

        else:
            current_Prices = getCurrentPrice(symbols)
            distribute_ticker_price(current_Prices)


def distribute_hourly_data(datadict):
    for symbol in datadict:
        ichimokuStatus = setInitialData(datadict[symbol])

def distribute_fourhour_data(datadict):
    for symbol in datadict:
        ichimokuStatus = setInitialData(datadict[symbol])

def distribute_daily_data(datadict):
    for symbol in datadict:
        ichimokuStatus = setInitialData(datadict[symbol])

def distribute_ticker_price(current_Prices):
    for data in current_Prices:
        calculateChange(float(data.price), data.symbol, 'h')
        calculateChange(float(data.price), data.symbol, 'q')
        calculateChange(float(data.price), data.symbol, 'd')

def getTime():
    return int(round(time.time() * 1000))


__main__()