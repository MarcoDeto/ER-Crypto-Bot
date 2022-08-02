def get_ichimoku(coin, interval, cross):
   return {
       'symbol': coin['symbol'],
       'time_frame': interval,
       'cross': cross.name,
       'close_price': {'$eq': None}
   }


def get_operation_number(coin, interval):
   return {
       'symbol': coin['symbol'],
       'time_frame': interval,
       'close_price': {'$ne': None}
   }


def get_open_ichimoku(coin, cross, interval):
   return {
       'symbol': coin['symbol'],
       'time_frame': interval,
       'status': 'OPEN',
       'cross': cross,
       'close_price': {'$eq': None}
   }


def get_long_trailing_stop(symbol, interval, price):
   return {
       'symbol': symbol,
       'status': 'OPEN',
       'cross': 'LONG',
       'time_frame': interval,
       'stop_min': {'$lt': price},
       'open_price': {'$lt': price},
       'close_price': {'$eq': None}
   }


def get_short_trailing_stop(symbol, interval, price):
   return {
       'symbol': symbol,
       'status': 'OPEN',
       'cross': 'SHORT',
       'time_frame': interval,
       'stop_min': {'$gt': price},
       'open_price': {'$gt': price},
       'close_price': {'$eq': None}
   }


def get_long_stop_loss(symbol, price):
    return {
        'symbol': symbol,
        'status': 'OPEN',
        'cross': 'LONG',
        'stop_loss': {'$gt': price},
        'close_price': {'$eq': None}
    }


def get_short_stop_loss(symbol, price):
    return {
        'symbol': symbol,
        'status': 'OPEN',
        'cross': 'SHORT',
        'stop_loss': {'$lt': price},
        'close_price': {'$eq': None}
    }


def get_long_take_profits(symbol, price):
    return {
        'symbol': symbol,
        'status': 'OPEN',
        'cross': 'LONG',
        'take_profit': {'$lt': price},
        'close_price': {'$eq': None}
    }


def get_short_take_profits(symbol, price):
    return {
        'symbol': symbol,
        'status': 'OPEN',
        'cross': 'SHORT',
        'take_profit': {'$gt': price},
        'close_price': {'$eq': None}
    }