# FARE RSI CON I VALORI DELLA CHIUSURA CANDELA [4] NON QUELLI DELLA LOW SHADOW

import numpy
import talib

def RSIIsAlert(close):
   price = close[0]
   rsi = talib.RSI(close, 5)
   if (rsi[len(rsi) - 1] > 80 or rsi[len(rsi) - 1] < 20):
      return True
   else:
      return False
