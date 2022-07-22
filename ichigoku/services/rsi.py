import talib
from models.enums import RSIType


def RSIIsAlert(close_prices):
   rsi = talib.RSI(close_prices, 5)
   if (rsi[-1] > 80):
      return RSIType.OVERBOUGHT
   elif (rsi[-1] < 20):
      return RSIType.OVERSOLD
   else:
      return None


def double_max_rsi(close_prices):
   rsi = talib.RSI(close_prices, 5)
   rsi_list = []
   for item in rsi:
      if (item > 0):
         rsi_list.append(item)
   get_list = rsi_list
   max_rsi = max(get_list)
   max_rsi_index = get_list.index(max_rsi)
   get_list.remove(max_rsi)
   min_range = max_rsi - max_rsi * 5 / 100
   max_range = max_rsi + max_rsi * 5 / 100
   second_max_rsi = max(rsi_list)
   if (max_rsi > 80 and second_max_rsi > 80):
      return True
   return False
   # massimo 10 candele
   # check i f i massimi sono sopra overbought  oversell
   # rsi deve essere sempre sopra a 80
   # controllare se c'è spazio in mezzo e se rsi
   # di quelle candele sia più basso del minimno più basso
