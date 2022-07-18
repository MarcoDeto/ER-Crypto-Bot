# FARE RSI CON I VALORI DELLA CHIUSURA CANDELA [4] NON QUELLI DELLA LOW SHADOW

import numpy
import talib

def RSIIsAlert(close):
   rsi = talib.RSI(close)
   if (rsi > 80 or rsi < 20):
      return True
   else:
      return False