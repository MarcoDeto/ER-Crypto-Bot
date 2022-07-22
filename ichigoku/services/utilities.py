
import time
import numpy as np
from config import *
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

    data_array = get_neccesaries(data)

    current_candels = data_array[:len(data_array) - 1]
    current_ichimoku = getIchimoku(current_candels, interval)

    last_candels = data_array[:len(data_array) - 2]
    last_ichimoku = getIchimoku(last_candels, interval)

    return (current_ichimoku, last_ichimoku)


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


def clickInterval(interval, intervals):
    match (interval):
        case '1m':
            intervals[5].click()
        case '3m':
            intervals[6].click()
        case '5m':
            intervals[7].click()
        case '15m':
            intervals[8].click()
        case '30m':
            intervals[9].click()
        case '45m':
            intervals[10].click()
        case '1h':
            intervals[11].click()
        case '2h':
            intervals[12].click()
        case '3h':
            intervals[13].click()
        case '4h':
            intervals[14].click()
        case '1d':
            intervals[15].click()
        case _:
            return