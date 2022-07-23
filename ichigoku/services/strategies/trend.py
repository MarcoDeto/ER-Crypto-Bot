from services.strategies.double import *
from models.enums import Trend


def get_interval_trend(data):
   current_candle = data[len(data)-1]
   first_candle = data[0]

   current_price = get_higher_value(current_candle[0], current_candle[4])
   old_price = get_higher_value(first_candle[0], first_candle[4])

   if (old_price > current_price):
      return Trend.DOWNTREND
   else:
      return Trend.UPTREND


def get_higher_value(x, y):
    if (float(x) > float(y)):
        return float(x)
    else:
        return float(y)


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
