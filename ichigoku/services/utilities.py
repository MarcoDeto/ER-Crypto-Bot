
import time
import numpy as np
from config import *
from datetime import datetime
from services.strategies.trend import get_interval_trend
from services.strategies.ichimoku import set_ichimoku


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


def set_initial_data(data, interval):

    data_array = get_neccesaries(data)

    current_candels = data_array[:len(data_array) - 1]
    current_ichimoku = set_ichimoku(current_candels, interval)

    trend = get_interval_trend(current_ichimoku)

    last_candels = data_array[:len(data_array) - 2]
    last_ichimoku = set_ichimoku(last_candels, interval)

    return (current_ichimoku, last_ichimoku, trend)


def distribute_data(datadict, interval):
    result = []
    for symbol in datadict:
        ichimokuStatus = set_initial_data(datadict[symbol], interval)
        result.append(ichimokuStatus)
    return result
    

def get_diff_percent(Xi, Xf, cross):
    if (cross == 'LONG'):
        return ((float(Xf) - float(Xi)) / float(Xi)) * 100
    if (cross == 'SHORT'):
        return ((float(Xi) - float(Xf)) / float(Xf)) * 100
    else:
        return 0


def get_diff_time(open, close):
    return close - open


def get_time():
    return int(round(time.time() * 1000))


def get_detect(timeDifference):
    timeStamp = (get_time() - timeDifference)
    result = []
    for interval in INTERVALS:
        result.append(int(timeStamp // get_delay(interval)))
    return result

def get_operation_info(operation, price):
   close_date = datetime.now()
   time = get_diff_time(operation['open_date'], close_date)
   diff = get_diff_percent(operation['open_price'], float(price), operation['cross'])
   percent = round(diff, 2)
   return (close_date, time, percent)

def get_delay(interval):
    match (interval):
        case '1m':
            return 10000
        case '3m':
            return 30000
        case '5m':
            return 50000
        case '15m':
            return 150000
        case '30m':
            return 300000
        case '1h':
            return 600000
        case '2h':
            return 1200000
        case '4h':
            return 2400000
        case '1d':
            return 14400000
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
