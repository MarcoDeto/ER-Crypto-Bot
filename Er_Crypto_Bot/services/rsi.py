# FARE RSI CON I VALORI DELLA CHIUSURA CANDELA [4] NON QUELLI DELLA LOW SHADOW

import numpy
import talib

def RSIIsAlert(close):
   rsi = talib.RSI(close)
   if (rsi > 80 or rsi < 20):
      return True
   else:
      return False

def checkDivergence():
   #30/70 per time_frame grandi come il bisettimanalke 
   #20/80 per tutti i TimeFrame più piccoli
   lower_barrier = 30
   upper_barrier = 70
   width = 5
   #Bullish Divergence
   for i in range(len(Data)):

      try:
      if Data.iloc[i, 4] < lower_barrier:
            for a in range(i + 1, i + width):
               if Data.iloc[a, 4] > lower_barrier:
                     for r in range(a + 1, a + width):
                        if Data.iloc[r, 4] < lower_barrier and Data.iloc[r, 4] > Data.iloc[i, 4] and Data.iloc[r, 3] < Data.iloc[i, 3]:
                           for s in range(r + 1, r + width): 
                              if Data.iloc[s, 4] > lower_barrier:
                                 print('Bullish above',Data.iloc[s+1,1])
                                 Data.iloc[s + 1, 5] = 1
                                 break
                              else:
                                 continue
                     else:
                           continue
               else:
                  continue
      else:
         continue
   except IndexError:
      pass
   #Bearish Divergence
   for i in range(len(Data)):
   try:
      if Data.iloc[i, 4] > upper_barrier:
         for a in range(i + 1, i + width): 
               if Data.iloc[a, 4] < upper_barrier:
                  for r in range(a + 1, a + width):
                     if Data.iloc[r, 4] > upper_barrier and Data.iloc[r, 4] < Data.iloc[i, 4] and Data.iloc[r, 3] > Data.iloc[i, 3]:
                           for s in range(r + 1, r + width):
                              if Data.iloc[s, 4] < upper_barrier:
                                 print('Bearish below',Data.iloc[s+1,2])
                                 Data.iloc[s + 1, 6] = -1
                                 break
                              else:
                                 continue
                     else:
                           continue
                  else:
                     continue
               else:
                  continue
   except IndexError:
      pass