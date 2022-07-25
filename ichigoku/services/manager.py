from services.database.mongoDB import *
from services.strategies.trend import *
from services.messages.messages import *
from services.messages.tradingview import *
from services.exchange.binance import *
from services.exchange.bybit import *


def open_operation(my_channel, ichimoku):
   link = None
   if (ichimoku.cross == 'LONG'):
      open_binance_order(ichimoku['symbol'], 10)
      link = get_trading_view_graph(
          ichimoku.time_frame, ichimoku.symbol, 'BINANCE')

   elif(ichimoku.cross == 'SHORT'):
      open_bybit_order(ichimoku.symbol, 10)
      link = get_trading_view_graph(
          ichimoku.time_frame, ichimoku.symbol, 'BYBIT')

   open_price = float(get_price(ichimoku.symbol))
   operation = get_insert_ichimoku(ichimoku, open_price)

   insert_ichiGoku(operation)
   send_open_messages(my_channel, link, operation)


def close_operation(my_channel, ichimoku, price, stop_loss=False):
   link = None
   if (ichimoku['cross'] == 'LONG'):
      close_binance_order(ichimoku['symbol'], 10)
      link = get_trading_view_graph(
          ichimoku['time_frame'], ichimoku['symbol'], 'BINANCE')

   elif(ichimoku['cross'] == 'SHORT'):
      close_bybit_order(ichimoku['symbol'], 10)
      link = get_trading_view_graph(
          ichimoku['time_frame'], ichimoku['symbol'], 'BYBIT')

   operation = get_take_profit(ichimoku, price)
   if (stop_loss == True):
      operation = get_stop_loss(ichimoku, price)

   update_ichiGoku(operation)
   send_close_messages(my_channel, link, operation, stop_loss)


def check_stop_loss(my_channel, symbol, interval, price):

   stop_losses = get_stop_losses(symbol, interval, price)
   for operation in stop_losses:
      print('STOP LOSS')
      close_operation(my_channel, operation, price, stop_loss=True)


def check_trading_stops(my_channel, symbol, interval, price, kijun_sen):
   
   trading_stops = get_trading_stops(symbol, interval, price, kijun_sen)
   for operation in trading_stops:
      print('TRADING STOP')
      close_operation(my_channel, operation, price)


def check_take_profit(my_channel, symbol, interval, price, close_prices):

   take_profits = []

   double_top_trend = is_double_top_trend(close_prices, interval)
   double_top_rsi = is_double_top_rsi(close_prices)
   if (double_top_trend == True and double_top_rsi == True):
      take_profits = get_long_take_profits(symbol, interval)
   
   double_bottom_trend = is_double_top_trend(close_prices, interval)
   double_bottom_rsi = is_double_top_rsi(close_prices)
   if (double_bottom_trend == True and double_bottom_rsi == True):
      take_profits = get_short_take_profits(symbol, interval)

   for operation in take_profits:
      print('TAKE PROFIT')
      close_operation(my_channel, operation, price)
   