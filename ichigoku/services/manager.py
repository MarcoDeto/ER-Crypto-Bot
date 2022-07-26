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
   tollerance = get_stop_loss_tollerance(ichimoku.time_frame)
   stop_min = (price + (price * 0.95 / 100))
   stop_loss = (price - (price * tollerance / 100))
   take_profit = (price + (price * (tollerance * 2) / 100))

   if (ichimoku.cross == CrossType.LONG):
      open_binance_order(ichimoku.symbol, 10, stop_loss)
      link = get_trading_view_graph(
          ichimoku.time_frame, ichimoku.symbol, 'BINANCE')

   elif(ichimoku.cross == CrossType.SHORT):
      stop_loss = (price + (price * tollerance / 100))
      take_profit = (price - (price * (tollerance * 2) / 100))
      open_bybit_order(ichimoku.symbol, 10, stop_loss)
      link = get_trading_view_graph(
          ichimoku.time_frame, ichimoku.symbol, 'BYBIT')
   
   operation = get_insert_ichimoku(ichimoku, price, stop_min, stop_loss, take_profit)

   insert_ichiGoku(operation)
   send_open_messages(telegram, link, operation)


def close_operation(telegram, ichimoku, price, status):
   link = None
   if (ichimoku['cross'] == 'LONG'):
      close_binance_order(ichimoku['symbol'], 10)
      link = get_trading_view_graph(
          ichimoku['time_frame'], ichimoku['symbol'], 'BINANCE')

   elif(ichimoku['cross'] == 'SHORT'):
      close_bybit_order(ichimoku['symbol'], 10)
      link = get_trading_view_graph(
          ichimoku['time_frame'], ichimoku['symbol'], 'BYBIT')

   operation = get_update_ichimoku(ichimoku, price, status)

   update_ichiGoku(operation)
   send_close_messages(telegram, link, operation, status)


def check_stop_losses(telegram, symbol, price):

   stop_losses = get_stop_losses(symbol, price)
   for operation in stop_losses:
      print('STOP LOSS')
      close_operation(telegram, operation, price, status='STOP LOSS')


def check_trailing_stops(telegram, symbol, interval, price, kijun_sen):
   
   trailing_stops = get_trailing_stops(symbol, interval, price, kijun_sen)
   for operation in trailing_stops:
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
   