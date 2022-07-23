
import time
import numpy as np
from config import *
from datetime import datetime
from services.strategies.trend import get_interval_trend
from services.strategies.ichimoku import getIchimoku


def get_neccesaries(datalist):
    returndata = []
    for window in datalist:
        returndata.append(list(map(float, window[2:5])))
    return np.array(returndata)


def get_close_prices(datalist):
    returndata = []
    for window in datalist:
        returndata.append(float(window[4]))
    return np.array(returndata)


def setInitialData(data, interval):

    data_array = get_neccesaries(data)

    trend = get_interval_trend(data)

    current_candels = data_array[:len(data_array) - 1]
    current_ichimoku = getIchimoku(current_candels, interval)

    last_candels = data_array[:len(data_array) - 2]
    last_ichimoku = getIchimoku(last_candels, interval)

    return (current_ichimoku, last_ichimoku, trend)


def distribute_data(datadict, interval):
    result = []
    for symbol in datadict:
        ichimokuStatus = setInitialData(datadict[symbol], interval)
        result.append(ichimokuStatus)
    return result
    

def diffPercent(Xi, Xf, cross):
    if (cross == 'LONG'):
        return ((float(Xf) - float(Xi)) / float(Xi)) * 100
    if (cross == 'SHORT'):
        return ((float(Xi) - float(Xf)) / float(Xf)) * 100
    else:
        return 0


def diffTime(open, close):
    return close - open


def getTime():
    return int(round(time.time() * 1000))


def getDetect(timeDifference):
    timeStamp = (getTime() - timeDifference)
    result = []
    for interval in INTERVALS:
        result.append(int(timeStamp // get_delay(interval)))
    return result

def get_operation_info(operation, price):
   close_date = datetime.now()
   time = diffTime(operation['open_date'], close_date)
   diff = diffPercent(operation['open_price'], float(price), operation['cross'])
   percent = round(diff, 2)
   return (close_date, time, percent)

def get_delay(interval):
    match (interval):
        case '1m':
            return 2500
        case '3m':
            return 7500
        case '5m':
            return 10000
        case '15m':
            return 12500
        case '30m':
            return 15000
        case '1h':
            return 27500
        case '2h':
            return 25000
        case '4h':
            return 27500
        case '1d':
            return 30000
        case _:
            return 1


def get_interval_index(interval):
    match (interval):
        case '1m':
            return 5
        case '3m':
            return 6
        case '5m':
            return 7
        case '15m':
            return 8
        case '30m':
            return 9
        case '45m':
            return 10
        case '1h':
            return 11
        case '2h':
            return 12
        case '3h':
            return 13
        case '4h':
            return 14
        case '1d':
            return 15
        case _:
            return


def get_timestap(interval):
    match (interval):
        case '1m':
            return 60 * 1000
        case '3m':
            return 60 * 3 * 1000
        case '5m':
            return 60 * 5 * 1000
        case '15m':
            return 60 * 15 * 1000
        case '30m':
            return 60 * 30 * 1000
        case '1h':
            return 60 * 60 * 1000
        case '2h':
            return 60 * 60 * 2 * 1000
        case '4h':
            return 60 * 60 * 4 * 1000
        case '1d':
            return 60 * 60 * 24 * 1000
        case _:
            return 1
