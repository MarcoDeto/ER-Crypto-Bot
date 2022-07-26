from services.strategies.ichimoku import Ichimoku
from services.strategies.double import *
from models.enums import Trend

'''
L’algoritmo comincia considerando quali siano gli swing points a rialzo e a ribasso 
per poter avere un elenco dei punti candidati a diventare estremi della linea da tracciare.

Gli swing points vengono determinati in questo modo:
Se PC(T0) > PC(T1) & PC(T2) > PC(T1) => PC(T1) è un punto di swing low
Se PC(T0) < PC(T1) & PC(T2) < PC(T1) => PC(T1) è un punto di swing high

Dove:
PC(T1) è il prezzo di chiusura di una candela sul grafico
PC(T0) è il prezzo di chiusura della candela precedente
PC(T2) è il prezzo di chiusura della candela successiva

L’algoritmo ripete questo calcolo su tutte le candele del grafico
per identificare quali si possano considerare degli swing point. 

A questo punto deve capire quali siano quelli tra cui tracciare la linea, 
per cui il passaggio successivo sarà:

Se PC(T) è uno swing high, controlla l’ultimo swing point;
In caso l’ultimo swing point fosse uno swing low, controlla se la differenza di 
prezzo tra i due punti è maggiore del parametro di deviazione selezionato dal trader;
Se la differenza è maggiore o uguale al parametro, traccia una linea tra i due punti;
Se la differenza è minore al parametro, ignora lo swing point;
In caso l’ultimo swing point fosse uno swing high, 
sostituisci il nuovo punto a quello precedente 
per tracciare la linea che parte dall’ultimo swing low.
'''

def get_zig_zag_trend(data):
    high_swings = []
    low_swings = []
    candel_index = -2
    prev_index = -3
    next_index = -1
    for candle in data:
        candel_price = data[candel_index][4]
        prev_price = data[prev_index][4]
        next_price = data[next_index][4]

        if (prev_price > candel_price and next_price > candel_price):
            low_swings.append( { 'index': candel_index, 'value': candel_price } )
        if (prev_price < candel_price and next_price < candel_price):
            high_swings.append( { 'index': candel_index, 'value': candel_price } )

        candel_index = candel_index - 1
        prev_index = prev_index - 1
        next_index = next_index - 1
    

    
    

def get_interval_trend(ichimoku: Ichimoku):

    if (ichimoku.senkou_span_B > ichimoku.close_price):
       return Trend.DOWNTREND
    else:
       return Trend.UPTREND


def is_double_top_trend(close_prices, interval):
 
    (trend_list, filtered) = get_trend_range(close_prices)
 
    tolerance = get_tolerance(interval)
    double_top = get_double_top(trend_list, filtered, tolerance)
    if double_top == None:
       return False
    else:
       return True


def is_double_bottom_trend(close_prices, interval):

   (trend_list, filtered) = get_trend_range(close_prices)

   tolerance = get_tolerance(interval)
   double_bottom = get_double_bottom(trend_list, filtered, tolerance)
   if double_bottom == None:
      return False
   else:
      return True


def get_trend_range(close_prices):
   trend_list = close_prices[-10:].tolist()
   filtered = close_prices[-10:].tolist()

   return (trend_list, filtered)


def get_tolerance(interval):
    match (interval):
        case '1m':
            return 0.05
        case '3m':
            return 0.10
        case '5m':
            return 0.15
        case '15m':
            return 0.3
        case '30m':
            return 0.5
        case '1h':
            return 0.7
        case '2h':
            return 1
        case '4h':
            return 1.2
        case '1d':
            return 1.7
        case _:
            return 0
