from models.enums import CrossType
from services.database.mongoDB import *
from services.strategies.trend import *
from services.messages.messages import *
from services.messages.tradingview import *
from services.exchange.binance import *
from services.exchange.bybit import *


def open_operation(telegram, ichimoku: Operation):
   link = None
   price = get_price(ichimoku.symbol)
   
   stop_min_tollerance = get_stop_min_tollerance(ichimoku.time_frame)
   stop_min = round((price + (price * stop_min_tollerance / 100)), 2)
   
   sl_tp_tollerance = get_sl_tp_tollerance(ichimoku.time_frame)
   stop_loss = round((price - (price * sl_tp_tollerance / 100)), 2)
   take_profit = round((price + (price * (sl_tp_tollerance * 2) / 100)), 2)
   side = 'Buy'

   if (ichimoku.cross == CrossType.LONG):
      #open_binance_order(ichimoku.symbol, 10, stop_loss)
      #order_placed = open_bybit_order(ichimoku.symbol, side, take_profit, stop_loss)
      order_placed = None
      link = get_trading_view_graph(
          ichimoku.time_frame, ichimoku.symbol, 'BINANCE')

   elif(ichimoku.cross == CrossType.SHORT):
      stop_min = round((price + (price * stop_min_tollerance / 100)), 2)
      stop_loss = round((price + (price * sl_tp_tollerance / 100)), 2)
      take_profit = round((price - (price * (sl_tp_tollerance * 2) / 100)), 2)
      side = 'Sell'
      #open_bybit_order(ichimoku.symbol, 10, stop_loss)
      #order_placed = open_bybit_order(ichimoku.symbol, side, take_profit, stop_loss)
      order_placed = None
      link = get_trading_view_graph(
          ichimoku.time_frame, ichimoku.symbol, 'BYBIT')

   operation = get_insert_ichimoku(ichimoku, price, side, stop_min, take_profit, stop_loss, order_placed)

   insert_ichiGoku(operation)
   send_open_messages(telegram, link, operation)


def close_operation(telegram, ichimoku, price, status):
   link = None
   orders = get_active_orders(ichimoku['symbol'])
   if (ichimoku['cross'] == 'LONG'):
      #close_binance_order(ichimoku['symbol'], 10)
      order_closed = close_bybit_order(ichimoku['symbol'], 'Sell', ichimoku['qty'])
      link = get_trading_view_graph(
          ichimoku['time_frame'], ichimoku['symbol'], 'BINANCE')

   elif(ichimoku['cross'] == 'SHORT'):
      #close_bybit_order(ichimoku['symbol'], 10)
      order_closed = close_bybit_order(ichimoku['symbol'], 'Buy', ichimoku['qty'])
      link = get_trading_view_graph(
          ichimoku['time_frame'], ichimoku['symbol'], 'BYBIT')

   operation = get_update_ichimoku(ichimoku, price, status)

   update_ichiGoku(operation)
   send_close_messages(telegram, link, operation, status)


def close_stop_losses(telegram, open_operations, price, senkou_span_A, senkou_span_B):
   
   stop_losses = get_stop_losses(open_operations, price, senkou_span_A, senkou_span_B)
   for operation in stop_losses:
      print('STOP LOSS')
      close_operation(telegram, operation, price, status='STOP LOSS')


def close_trailing_stops(telegram, open_operartions, price, kijun_sen):

   #trailing_stops = get_trailing_stops(symbol, interval, price, kijun_sen)
   for operation in open_operartions:
      if price > operation['stop_min'] and operation['cross'] == 'LONG' and price < kijun_sen:
         print('TRAILING STOP')
         close_operation(telegram, operation, price, status='TRAILING STOP')
      if price < operation['stop_min'] and operation['cross'] == 'SHORT' and price > kijun_sen:
         print('TRAILING STOP')
         close_operation(telegram, operation, price, status='TRAILING STOP')


def check_take_profits(telegram, symbol, interval, price, close_prices):

   take_profits = get_take_profits(symbol, price)
   for operation in take_profits:
      print('TAKE PROFIT')
      close_operation(telegram, operation, price, status='TAKE PROFIT')

   take_profits = []

   double_top_trend = is_double_top_trend(close_prices, interval)
   double_top_rsi = is_double_top_rsi(close_prices)
   if (double_top_trend == True and double_top_rsi == True):
      take_profits = get_double_take_profits(symbol, 'LONG', interval)

   double_bottom_trend = is_double_bottom_trend(close_prices, interval)
   double_bottom_rsi = is_double_bottom_rsi(close_prices)
   if (double_bottom_trend == True and double_bottom_rsi == True):
      take_profits = get_double_take_profits(symbol, 'SHORT', interval)

   for operation in take_profits:
      print('DB TAKE PROFIT')
      close_operation(telegram, operation, price, status='DB TAKE PROFIT')
