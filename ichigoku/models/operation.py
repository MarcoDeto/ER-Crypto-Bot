
from bson import ObjectId  # pip3 install pymongo
from datetime import datetime
from services.exchange.binance import *
from services.utilities import get_operation_info


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


def get_insert_ichimoku(operation: Operation, open_price, side, stop_min, take_profit, stop_loss, order_placed):
   if order_placed ==  None:
      return {
       '_id': ObjectId(),
       'order_id': '',
       'symbol': operation.symbol,
       'base': operation.base,
       'quote': operation.quote,
       'isMarginTrade': operation.isMarginTrade,
       'isBuyAllowed': operation.isBuyAllowed,
       'isSellAllowed': operation.isSellAllowed,
       'open_price': open_price,
       'qty': '',
       'order_status': '',
       'cum_exec_fee': '',
       'close_price': None,
       'open_date': datetime.now(),
       'close_date': None,
       'operation_number': operation.operation_number,
       'cross': operation.cross.name,
       'side': '',
       'time_frame': operation.time_frame,
       'percent': 0,
       'seconds': 0,
       'status': 'OPEN',
       'stop_min': round(stop_min, 2),
       'stop_loss': round(stop_loss, 2),
       'take_profit': round(take_profit, 2)
      }
   else :
      return {
       '_id': ObjectId(),
       'order_id': order_placed['order_id'],
       'symbol': operation.symbol,
       'base': operation.base,
       'quote': operation.quote,
       'isMarginTrade': operation.isMarginTrade,
       'isBuyAllowed': operation.isBuyAllowed,
       'isSellAllowed': operation.isSellAllowed,
       'open_price': open_price,
       'qty': order_placed['qty'],
       'order_status': order_placed['order_status'],
       'cum_exec_fee': order_placed['cum_exec_fee'],
       'close_price': None,
       'open_date': datetime.now(),
       'close_date': None,
       'operation_number': operation.operation_number,
       'cross': operation.cross.name,
       'side': order_placed['side'],
       'time_frame': operation.time_frame,
       'percent': 0,
       'seconds': 0,
       'status': 'OPEN',
       'stop_min': round(stop_min, 2),
       'stop_loss': round(order_placed['stop_loss'], 2),
       'take_profit': round(order_placed['take_profit'], 2)
      }


def get_update_ichimoku(operation, price, status):
   (close_date, time, percent) = get_operation_info(operation, price)
   return {
       '_id': operation['_id'],
       'order_id': operation['order_id'],
       'symbol': operation['symbol'],
       'base': operation['base'],
       'quote': operation['quote'],
       'isMarginTrade': operation['isMarginTrade'],
       'isBuyAllowed': True,
       'isSellAllowed': True,
       'open_price': operation['open_price'],
       'qty': operation['qty'],
       'order_status': operation['order_status'],
       'cum_exec_fee': operation['cum_exec_fee'],
       'close_price': float(price),
       'open_date': operation['open_date'],
       'close_date': close_date,
       'operation_number': operation['operation_number'],
       'cross': operation['cross'],
       'side': operation['side'],
       'time_frame': operation['time_frame'],
       'percent': percent,
       'seconds': time.seconds,
       'status': status,
       'stop_min': operation['stop_min'],
       'stop_loss': operation['stop_loss'],
       'take_profit': operation['take_profit'],
   }
