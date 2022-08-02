from hashlib import new
from services.settings import *
from services.strategies.ichimoku import Ichimoku
from services.strategies.double import *
from models.enums import Trend


def inverts_data(data):
    new_data = []
    index = 1
    for x in data:
        new_data.append(data[len(data)-index])
        index = index + 1
    return new_data


def get_swings(data, interval):

    low_swings = []
    high_swings = []

    new_data = inverts_data(data)

    swing_index = 0
    next_index = 1
    curr = new_data[swing_index]
    next = new_data[next_index]
    high = 0
    low = 0
    low_index = 0
    high_index = 0
    if float(curr[4]) > float(next[4]):
        high = curr
        low = next
    else:
        low = curr
        high = next

    for x in new_data:

        next_index = next_index + 1
        if next_index >= len(new_data):
            continue
        next = new_data[next_index]
        next_price = float(next[4])

        if next_price < float(low[4]):
            low = next
        elif next_price > float(high[4]):
            high = next

        if is_to_be_ignored(high[4], low[4], interval) == True:
            continue

        low_index = new_data.index(low)
        high_index = new_data.index(high)

        if len(low_swings) > 0:
            last_low_swing_index = low_swings[len(low_swings)-1]['index']

        if len(high_swings) > 0:
            last_high_swing_index = high_swings[len(high_swings)-1]['index']

        if low_index > high_index:

            if len(high_swings) != 0:
                if len(low_swings) == 0:
                    low_swings.append({'index': low_index, 'value': low})
                elif last_low_swing_index != low_index:
                    if len(low_swings) >= len(high_swings):
                        if low_index > last_high_swing_index and last_low_swing_index > last_high_swing_index:
                            low_swings.remove(low_swings[len(low_swings)-1])
                        low_swings.append({'index': low_index, 'value': low})

            if len(high_swings) <= len(low_swings):
                if len(high_swings) == 0:
                    high_swings.append({'index': high_index, 'value': high})
                elif last_high_swing_index != high_index:
                    if len(low_swings) >= len(high_swings):
                        if high_index > last_low_swing_index and last_high_swing_index > last_low_swing_index:
                            high_swings.remove(high_swings[len(high_swings)-1])
                        high_swings.append(
                            {'index': high_index, 'value': high})

        if high_index > low_index:

            if len(low_swings) != 0:
                if len(high_swings) == 0:
                    high_swings.append({'index': high_index, 'value': high})
                elif last_high_swing_index != high_index:
                    if len(low_swings) >= len(high_swings):
                        if high_index > last_low_swing_index and last_high_swing_index > last_low_swing_index:
                            high_swings.remove(high_swings[len(high_swings)-1])
                        high_swings.append(
                            {'index': high_index, 'value': high})

            if len(low_swings) <= len(high_swings):
                if len(low_swings) == 0:
                    low_swings.append({'index': low_index, 'value': low})
                elif low_swings[len(low_swings)-1]['index'] != low_index:
                    if len(low_swings) >= len(high_swings):
                        if low_index > last_high_swing_index and last_low_swing_index > last_high_swing_index:
                            low_swings.remove(low_swings[len(low_swings)-1])
                        low_swings.append({'index': low_index, 'value': low})

    print(interval)

    if len(high_swings) == 0 and len(low_swings) == 0:
        low_swings.append({'index': low_index, 'value': low})
        high_swings.append({'index': high_index, 'value': high})

    if float(low[4]) < float(low_swings[len(low_swings)-1]['value'][4]):
        if len(low_swings) > len(high_swings):
            low_swings.remove(low_swings[len(low_swings)-1])
            low_swings.append({'index': low_index, 'value': low})

    if float(high[4]) > float(high_swings[len(high_swings)-1]['value'][4]):
        if len(low_swings) < len(high_swings):
            high_swings.remove(high_swings[len(high_swings)-1])
            high_swings.append({'index': high_index, 'value': high})

    return (low_swings, high_swings)


def get_trend(data, interval):

    (low_swings, high_swings) = get_swings(data, interval)

    low_index = low_swings[0]['index']
    high_index = high_swings[0]['index']

    low_price = float(low_swings[0]['value'][4])
    high_price = float(high_swings[0]['value'][4])

    current_price = float(data[-1][4])

    if low_index < 10 and high_index >= 10:
        if high_price - low_price > 0:
            return Trend.DOWNTREND
        else:
            return Trend.UPTREND

    elif high_index < 10 and low_index >= 10:
        if low_price - high_price > 0:
            return Trend.DOWNTREND
        else:
            return Trend.UPTREND

    elif high_index >= 10 and low_index >= 10:
        if low_index < high_index:
            if low_price - current_price < 0:
                return Trend.UPTREND
            else:
                return Trend.DOWNTREND

        if high_index < low_index:
            if high_price - current_price > 0:
                return Trend.DOWNTREND
            else:
                return Trend.UPTREND

    return None


def is_to_be_ignored(Xi, Xf, interval):
    # controlla se la differenza di  prezzo tra i due punti
    # è maggiore del parametro di deviazione selezionato dal trader

    diff = ((float(Xi) - float(Xf)) / float(Xf)) * 100

    swing_tollerange = get_swing_tollerange(interval)
    # Se la differenza è maggiore o uguale al parametro, traccia una linea tra i due punti;
    # Se la differenza è minore al parametro, ignora lo swing point;
    if (diff > 0 and diff >= swing_tollerange) or (diff < 0 and diff <= -(swing_tollerange)):
        return False
    else:
        return True


def get_interval_trend(ichimoku: Ichimoku):

    if (ichimoku.senkou_span_B > ichimoku.close_price):
       return Trend.DOWNTREND
    else:
       return Trend.UPTREND


def is_double_top_trend(close_prices, interval):

    (trend_list, filtered) = get_trend_range(close_prices)

    tolerance = get_dt_db_tolerance(interval)
    double_top = get_double_top(trend_list, filtered, tolerance)
    if double_top == None:
       return False
    else:
       return True


def is_double_bottom_trend(close_prices, interval):

   (trend_list, filtered) = get_trend_range(close_prices)

   tolerance = get_dt_db_tolerance(interval)
   double_bottom = get_double_bottom(trend_list, filtered, tolerance)
   if double_bottom == None:
      return False
   else:
      return True


def get_trend_range(close_prices):
   trend_list = close_prices[-10:].tolist()
   filtered = close_prices[-10:].tolist()

   return (trend_list, filtered)
