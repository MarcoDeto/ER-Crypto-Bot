
import time
import numpy as np
from config import *
from services.mongoDB import getIchimokuDB
from models.ichimoku import getIchimoku


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
    dataArray = get_neccesaries(data)
    currentIchimoku = getIchimoku(dataArray, interval)
    lastIchimoku = getIchimoku(dataArray[:len(dataArray) - 2], interval)
    return (currentIchimoku, lastIchimoku)


def diffPercent(Xi, Xf, cross):
    if (cross == 'LONG'):
        return ((float(Xf) - float(Xi)) / float(Xi)) * 100
    if (cross == 'SHORT'):
        return ((float(Xi) - float(Xf)) / float(Xf)) * 100
    else:
        return 0


def diffTime(open, close):
    return close - open


def getOperationDB(coin, interval):
    operationDB = getIchimokuDB(coin, interval)
    if (operationDB):
        return operationDB
    return coin


def getTime():
    return int(round(time.time() * 1000))


def getDetect(timeDifference):
    timeStamp = (getTime() - timeDifference)
    result = []
    for interval in INTERVALS:
        result.append(int(timeStamp // getDelay(interval)))
    return result


def getDelay(interval):
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
