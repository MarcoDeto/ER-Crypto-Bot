
from bson import ObjectId
from datetime import datetime
from services.exchange.binance import *
from services.utilities import diffPercent, diffTime, get_operation_info


class Operation:
   def __init__(self, _id, symbol, base, quote, isMarginTrade, isBuyAllowed, isSellAllowed, operation_number, cross, operation_type, time_frame):
      self._id = _id
      self.symbol = symbol
      self.base = base
      self.quote = quote
      self.isMarginTrade = isMarginTrade
      self.isBuyAllowed = isBuyAllowed
      self.isSellAllowed = isSellAllowed
      self.operation_number = operation_number
      self.cross = cross
      self.operation_type = operation_type
      self.time_frame = time_frame


def get_insert_ichimoku(operation: Operation, open_price):
   return {
       '_id': ObjectId(),
       'symbol': operation.symbol,
       'base': operation.base,
       'quote': operation.quote,
       'isMarginTrade': operation.isMarginTrade,
       'isBuyAllowed': operation.isBuyAllowed,
       'isSellAllowed': operation.isSellAllowed,
       'open_price': open_price,
       'close_price': None,
       'open_date': datetime.now(),
       'close_date': None,
       'operation_number': operation.operation_number,
       'cross': operation.cross.name,
       'time_frame': operation.time_frame,
       'percent': 0,
       'seconds': 0,
       'status': 'OPEN',
       'stop_loss': False,
   }


def get_take_profit(operation, price):
   (close_date, time, percent) = get_operation_info(operation, price)
   return {
       '_id': operation['_id'],
       'symbol': operation['symbol'],
       'base': operation['base'],
       'quote': operation['quote'],
       'isMarginTrade': operation['isMarginTrade'],
       'isBuyAllowed': True,
       'isSellAllowed': True,
       'open_price': operation['open_price'],
       'close_price': float(price),
       'open_date': operation['open_date'],
       'close_date': close_date,
       'operation_number': operation['operation_number'],
       'cross': operation['cross'],
       'time_frame': operation['time_frame'],
       'percent': percent,
       'seconds': time.seconds,
       'status': 'CLOSE',
       'stop_loss': False
   }

def get_stop_loss(operation: Operation, price):
   (close_date, time, percent) = get_operation_info(operation, price)
   return {
       '_id': operation['_id'],
       'symbol': operation['symbol'],
       'base': operation['base'],
       'quote': operation['quote'],
       'isMarginTrade': operation['isMarginTrade'],
       'isBuyAllowed': True,
       'isSellAllowed': True,
       'open_price': operation['open_price'],
       'close_price': float(price),
       'open_date': operation['open_date'],
       'close_date': close_date,
       'operation_number': operation['operation_number'],
       'cross': operation['cross'],
       'time_frame': operation['time_frame'],
       'percent': percent,
       'seconds': time.seconds,
       'status': 'CLOSE',
       'stop_loss': True
   }