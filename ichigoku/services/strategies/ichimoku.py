import numpy as np #pip install numpy
from config import ICHIMOKU_PARAMS

from services.strategies.rsi import *

data_array = np.array([0])
ichimokuStatus = False
low = 0
high = 0

class Ichimoku:
    def __init__(self, interval, tenkan_sen, kijun_sen, senkou_span_A, senkou_span_B, high, low, close_price):
        self.interval = interval
        self.tenkan_sen = tenkan_sen
        self.kijun_sen = kijun_sen
        self.senkou_span_A = senkou_span_A
        self.senkou_span_B = senkou_span_B
        self.high = high
        self.low = low
        self.close_price = close_price


def set_ichimoku(data_array, interval):

    # ICHIMOKU_PARAMS = getIchimokuParams(interval)
    tenkan_sen = get_tenkan_sen(data_array)
    kijun_sen = get_kijun_sen(data_array)
    senkou_span_A = get_senkou_span_A(data_array)
    senkou_span_B = get_senkou_span_B(data_array)

    high = data_array[:,0][-1]
    low = data_array[:,1][-1]
    close_price = data_array[:,2][-1]

    return Ichimoku(interval, tenkan_sen, kijun_sen, senkou_span_A, senkou_span_B, high, low, close_price)


def get_tenkan_sen(data_array):
    short_max = data_array[:,0][-ICHIMOKU_PARAMS[0]:].max()
    short_min = data_array[:,1][-ICHIMOKU_PARAMS[0]:].min()
    return (short_max + short_min)/2

def get_kijun_sen(data_array):
    medium_max = data_array[:,0][-ICHIMOKU_PARAMS[1]:].max()
    medium_min = data_array[:,1][-ICHIMOKU_PARAMS[1]:].min()
    return (medium_max + medium_min)/2

def get_senkou_span_A(data_array):
    # Torna indietro di N candele
    data = data_array[:-ICHIMOKU_PARAMS[1] - 1]
    tenkan_sen = get_tenkan_sen(data)
    kijun_sen = get_kijun_sen(data)
    return (tenkan_sen + kijun_sen)/2

def get_senkou_span_B(data_array):
    # Torna indietro di N candele
    start_index = -( ICHIMOKU_PARAMS[2] + ICHIMOKU_PARAMS[1])
    end_index = -( ICHIMOKU_PARAMS[1])
    long_max = data_array[:,0][start_index:end_index].max()
    lonh_min = data_array[:,1][start_index:end_index].min()
    return (long_max + lonh_min)/2