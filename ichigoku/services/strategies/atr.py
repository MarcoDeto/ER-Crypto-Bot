import numpy as np
import talib


def get_all_prices(data):
   high_prices = []
   low_prices = []
   close_prices = []
   for candle in data:
       high_prices.append(float(candle[2]))
       low_prices.append(float(candle[3]))
       close_prices.append(float(candle[4]))
   return (np.array(high_prices), np.array(low_prices), np.array(close_prices))


def get_ATR(data):
   (high_prices, low_prices, close_prices) = get_all_prices(data)
   return talib.ATR(high_prices, low_prices, close_prices, timeperiod=12)
