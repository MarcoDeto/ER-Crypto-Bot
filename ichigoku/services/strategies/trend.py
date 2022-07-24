from services.strategies.ichimoku import Ichimoku
from services.strategies.double import *
from models.enums import Trend


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
