from datetime import datetime
from bson import ObjectId  # pip3 install pymongo
from services.exchange.binance import get_price
from services.utilities import get_diff_time, get_diff_percent
from models.operation import Operation


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


def get_long_trading_stop(symbol, interval, price):
   return {
       'symbol': symbol,
       'status': 'OPEN',
       'cross': 'LONG',
       'time_frame': interval,
       'stop_min': {'$lt': price},
       'close_price': {'$eq': None}
   }


def get_short_trading_stop(symbol, interval, price):
   return {
       'symbol': symbol,
       'status': 'OPEN',
       'cross': 'SHORT',
       'time_frame': interval,
       'stop_min': {'$gt': price},
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