from datetime import datetime
import numpy as np

from services.rsi import *

dataArray = np.array([0])
ichimokuStatus = False
current_low = 0
current_high = 0

class Ichimoku:
    def __init__(self, tenkan_sen, kijun_sen, senkou_span_A, senkou_span_B, current_high, current_low, close_price):
        self.tenkan_sen = tenkan_sen
        self.kijun_sen = kijun_sen
        self.senkou_span_A = senkou_span_A
        self.senkou_span_B = senkou_span_B
        self.current_high = current_high
        self.current_low = current_low
        self.close_price = close_price


def getIchimoku(dataArray, interval):
    ICHIMOKU_PARAMS = getIchimokuParams(interval)
    tenkan_sen = ((dataArray[:,0][-ICHIMOKU_PARAMS[0]:].max()) + (dataArray[:,1][-ICHIMOKU_PARAMS[0]:].min()))/2
    kijun_sen = ((dataArray[:,0][-ICHIMOKU_PARAMS[1]:].max()) + (dataArray[:,1][-ICHIMOKU_PARAMS[1]:].min()))/2
    senkou_span_A = (tenkan_sen + kijun_sen) / 2
    senkou_span_B = ((dataArray[:,0][-ICHIMOKU_PARAMS[2]:].max()) + (dataArray[:,1][-ICHIMOKU_PARAMS[2]:].min()))/2
    current_high = dataArray[:,0][-1]
    current_low = dataArray[:,1][-1]
    close_price = dataArray[:,2][-1]
    return Ichimoku(tenkan_sen, kijun_sen, senkou_span_A, senkou_span_B, current_high, current_low, close_price)


def getIchimokuParams(interval):
    match (interval):
        case '1m':
            return [60, 20, 160, 30]
        case '3m':
            return [60, 20, 160, 30]
        case '5m':
            return [60, 20, 160, 30]
        case '15m':
            return [26, 9, 52, 26]
        case '30m':
            return [26, 9, 52, 26]
        case '1h':
            return [26, 9, 52, 26]
        case '2h':
            return [26, 9, 52, 26]
        case '4h':
            return [26, 9, 52, 26]
        case '1d':
            return [26, 9, 52, 26]
        case _:
            return None
