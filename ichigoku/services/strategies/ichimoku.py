import numpy as np
from config import ICHIMOKU_PARAMS

from services.strategies.rsi import *

dataArray = np.array([0])
ichimokuStatus = False
current_low = 0
current_high = 0

class Ichimoku:
    def __init__(self, interval, tenkan_sen, kijun_sen, senkou_span_A, senkou_span_B, current_high, current_low, close_price):
        self.interval = interval
        self.tenkan_sen = tenkan_sen
        self.kijun_sen = kijun_sen
        self.senkou_span_A = senkou_span_A
        self.senkou_span_B = senkou_span_B
        self.current_high = current_high
        self.current_low = current_low
        self.close_price = close_price


def getIchimoku(dataArray, interval):

    # ICHIMOKU_PARAMS = getIchimokuParams(interval)

    short_max = dataArray[:,0][-ICHIMOKU_PARAMS[0]:].max()
    short_min = dataArray[:,1][-ICHIMOKU_PARAMS[0]:].min()
    tenkan_sen = (short_max + short_min)/2

    medium_max = dataArray[:,0][-ICHIMOKU_PARAMS[1]:].max()
    medium_min = dataArray[:,1][-ICHIMOKU_PARAMS[1]:].min()
    kijun_sen = (medium_max + medium_min)/2
    
    senkou_span_A = (tenkan_sen + kijun_sen)/2
    # torna indietro di n candele
    start_index = -( ICHIMOKU_PARAMS[2] + ICHIMOKU_PARAMS[1] - 1 )
    end_index = -( ICHIMOKU_PARAMS[1] - 1 )
    long_max = dataArray[:,0][start_index:end_index].max()
    lonh_min = dataArray[:,1][start_index:end_index].min()
    senkou_span_B = (long_max + lonh_min)/2

    current_high = dataArray[:,0][-1]
    current_low = dataArray[:,1][-1]
    close_price = dataArray[:,2][-1]

    return Ichimoku(interval, tenkan_sen, kijun_sen, senkou_span_A, senkou_span_B, current_high, current_low, close_price)


def getIchimokuParams(interval):
    match (interval):
        case '1m':
            return [20, 60, 160]
        case '3m':
            return [20, 60, 160]
        case '5m':
            return [20, 60, 160]
        case '15m':
            return [9, 26, 52]
        case '30m':
            return [9, 26, 52]
        case '1h':
            return [9, 26, 52]
        case '2h':
            return [9, 26, 52]
        case '4h':
            return [9, 26, 52]
        case '1d':
            return [9, 26, 52]
        case _:
            return None
