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