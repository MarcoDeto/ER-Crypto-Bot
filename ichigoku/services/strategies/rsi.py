import talib
from config import ICHIMOKU_PARAMS
from services.strategies.double import *
from models.enums import RSIType


def RSI_is_alert(close_prices):
   rsi = talib.RSI(close_prices, 5)
   if (rsi[-1] > 80):
      return RSIType.OVERBOUGHT
   elif (rsi[-1] < 20):
      return RSIType.OVERSOLD
   else:
      return None


def is_double_top_rsi(close_prices):
   rsi = talib.RSI(close_prices, 5)

   (rsi_list, filtered) = get_rsi_range(rsi)

   for value in rsi:
      if (value < 80): return False

   double_top = get_double_top(rsi_list, filtered, tolerance=5)
   if double_top == None:
      return False
   else:
      return True


def is_double_bottom_rsi(close_prices):
   rsi = talib.RSI(close_prices, 5)

   (rsi_list, filtered) = get_rsi_range(rsi)

   for value in rsi:
      if (value > 20): return False

   double_bottom = get_double_bottom(rsi_list, filtered, tolerance=5)
   if double_bottom == None:
      return False
   else:
      return True


def get_rsi_range(rsi):
   rsi_list = []
   filtered = []
   for item in rsi:
      if (item > 0):
         filtered.append(item)
         rsi_list.append(item)

   start_index = -( ICHIMOKU_PARAMS[2] + 10)
   end_index = -( ICHIMOKU_PARAMS[2] )
   rsi_list = rsi_list[ start_index : end_index ]
   filtered = filtered[ start_index : end_index ]

   return (rsi_list,filtered)