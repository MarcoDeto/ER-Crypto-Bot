
import time
import numpy as np
from config import *
from datetime import datetime
from services.settings import *
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


def is_resp_tolerance(interval, price, span_B):
    max_tollerance = get_open_tollerance(interval)
    differece = 0
    if float(price) > float(span_B):
        differece = ((float(price) - float(span_B)) / float(span_B)) * 100
    else:
        differece = ((float(span_B) - float(price)) / float(price)) * 100
    
    if differece > max_tollerance:
        return False
    
    return True



