
from bson import ObjectId  # pip3 install pymongo
from pymongo import MongoClient  # pip3 install "pymongo[srv]"
from datetime import datetime

import pymongo
from services.telegram import sendMessage
from config import CONNECTION_STRING
from models.operation import Operation
from services.binance import *


def getConnection():
   while True:
      try:
         client = MongoClient(CONNECTION_STRING)
         mongoDB = client['Er_Crypto_Bot']
         collection = mongoDB['EMAs']
         return collection
      except:
         continue


def getEMAs():

   collection = getConnection()
   item_details = collection.find()
   result = []
   for item in item_details:
      result.append(item)
   return result


def getEMA(coin, main_ema, second_ema, interval):

   collection = getConnection()
   query = {
      'symbol': coin['symbol'],
      "ema_main": main_ema, 
      "ema_second": second_ema, 
      'time_frame': interval,
      'close_price': { '$eq': None }
   }
   item_details = collection.find(query).sort('open_date', pymongo.DESCENDING)
   result = {}
   i = 0
   for item in item_details:
      result[i] = item
      i = i+1
   if (len(result) > 0):
      return result[0]
   return result


def getOperationNumber(coin, main_ema, second_ema, interval):
   collection = getConnection()
   query = {
      'symbol': coin['symbol'],
      "ema_main": main_ema, 
      "ema_second": second_ema, 
      'time_frame': interval,
      'close_price': { '$ne': None }
   }
   result = collection.count_documents(query)
   return result + 1

async def insertEMA(operation: Operation):
   print('INSERT\n')
   collection = getConnection()
   EMA = {
       '_id': ObjectId(),
       'symbol': operation.symbol,
       'base': operation.base,
       'quote': operation.quote,
       'isMarginTrade': operation.isMarginTrade,
       'isBuyAllowed': operation.isBuyAllowed,
       'isSellAllowed': operation.isSellAllowed,
       'open_price': float(getPrice(operation.symbol)),
       'close_price': None,
       'open_date': datetime.now(),
       'close_date': None,
       'operation_number': operation.operation_number,
       'cross': operation.cross.name,
       'ema_main': operation.ema_main,
       'ema_second': operation.ema_second,
       'time_frame': operation.time_frame,
       'percent': 0,
       'seconds': 0,
       'status': operation.operation_type.name,
   }
   collection.insert_one(EMA)
   #adjust_leverage(operation.symbol)
   #adjust_margintype(operation.symbol)
   if (operation.cross.name == 'LONG'):
      open_order(operation.symbol, 'BUY', 10)
   if (operation.cross.name == 'SHORT'):
      open_order(operation.symbol, 'SELL', 10)


async def updateEMA(operation: Operation, coin: Operation, my_channel):
   print('UPDATE')
   collection = getConnection()
   open_price = coin['open_price']
   symbol = coin['symbol']
   close_price = float(getPrice(symbol))
   open_date = coin['open_date']
   close_date = datetime.now()
   cross = coin['cross']
   percent = round(diffPercent(open_price, close_price, cross), 2)
   time = diffTime(open_date, close_date)
   EMA = {
       '_id': coin['_id'],
       'symbol': symbol,
       'base': coin['base'],
       'quote': coin['quote'],
       'isMarginTrade': coin['isMarginTrade'],
       'isBuyAllowed': operation.isBuyAllowed,
       'isSellAllowed': operation.isSellAllowed,
       'open_price': open_price,
       'close_price': close_price,
       'open_date': open_date,
       'close_date': close_date,
       'operation_number': coin['operation_number'],
       'cross': cross,
       'ema_main': coin['ema_main'],
       'ema_second': coin['ema_second'],
       'time_frame': coin['time_frame'],
       'percent': percent,
       'seconds': time.seconds,
       'status': operation.operation_type.name,
   }
   collection.update_one({'_id': coin['_id']}, {"$set": EMA}, upsert=False)
   #adjust_leverage(symbol)
   #adjust_margintype(symbol)
   if (cross == 'LONG'):
      open_order(symbol, 'SELL', 10)
   if (cross == 'SHORT'):
      open_order(symbol, 'BUY', 10)
   await sendMessage(my_channel, symbol, cross, open_date, open_price, close_price, percent, time.seconds)


async def checkStopLoss(symbol, price):
   collection = getConnection()
   query = {
      'symbol': symbol,
      "status": 'OPEN', 
      "cross": 'LONG', 
      'open_price': { '$lt': price },
   }
   item_details = collection.find(query)
   result = []
   for item in item_details:
      result.append(item)
      query = {
      'symbol': symbol,
      "status": 'OPEN', 
      "cross": 'SHORT', 
      'open_price': { '$gt': price },
   }
   item_details = collection.find(query)
   for operation in result:
      print('STOP LOSS')
      collection = getConnection()
      open_price = operation['open_price']
      close_price = float(getPrice(operation['symbol']))
      open_date = operation['open_date']
      close_date = datetime.now()
      percent = round(diffPercent(open_price, close_price, operation['cross']), 2)
      time = diffTime(open_date, close_date)
      EMA = {
         '_id': operation['_id'],
         'symbol': operation['symbol'],
         'base': operation['base'],
         'quote': operation['quote'],
         'isMarginTrade': operation['isMarginTrade'],
         'isBuyAllowed': operation['isBuyAllowed'],
         'isSellAllowed': operation['isSellAllowed'],
         'open_price': open_price,
         'close_price': close_price,
         'open_date': open_date,
         'close_date': close_date,
         'operation_number': operation['operation_number'],
         'cross': operation['cross'],
         'ema_main': operation['ema_main'],
         'ema_second': operation['ema_second'],
         'time_frame': operation['time_frame'],
         'percent': percent,
         'seconds': time.seconds,
         'status': operation['status'],
      }
      collection.update_one({'_id': operation['_id']}, {"$set": EMA}, upsert=False)



def dropCollection():
   collection = getConnection()
   collection.drop()
