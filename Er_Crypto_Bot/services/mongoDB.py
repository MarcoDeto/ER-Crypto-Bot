
from bson import ObjectId  # pip3 install pymongo
from pymongo import MongoClient  # pip3 install "pymongo[srv]"
from datetime import datetime

import pymongo
from config import CONNECTION_STRING, MAIN_EMA
from models.operation import Operation
from services.binance import diffPercent, diffTime, getPrice


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


def getEMA(coin, second_ema, interval):

   collection = getConnection()
   query = {'symbol': coin['symbol'],
      "ema_second": second_ema, 'time_frame': interval}
   item_details = collection.find(query).sort('open_date', pymongo.DESCENDING)
   result = {}
   i = 0
   for item in item_details:
      result[i] = item
      i = i+1
   if (len(result) > 0):
      return result[0]
   return result


def insertEMA(operation: Operation, candle):
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
       'ema_main': MAIN_EMA,
       'ema_second': operation.ema_second,
       'time_frame': operation.time_frame,
       'percent': 0,
       'seconds': 0,
       'status': operation.operation_type.name,
   }
   return collection.insert_one(EMA)


def updateEMA(operation: Operation, coin: Operation, candle):
   print('UPDATE')
   collection = getConnection()
   open_price = coin['open_price']
   open_date = coin['open_date']
   close_date = datetime.now()
   percent = round(diffPercent(open_price, candle[4]), 2)
   time = diffTime(open_date, close_date)
   EMA = {
       '_id': coin['_id'],
       'symbol': coin['symbol'],
       'base': coin['base'],
       'quote': coin['quote'],
       'isMarginTrade': coin['isMarginTrade'],
       'isBuyAllowed': operation.isBuyAllowed,
       'isSellAllowed': operation.isSellAllowed,
       'open_price': open_price,
       'close_price': float(getPrice(coin['symbol'])),
       'open_date': open_date,
       'close_date': close_date,
       'operation_number': coin['operation_number'],
       'cross': coin['cross'],
       'ema_main': MAIN_EMA,
       'ema_second': coin['ema_second'],
       'time_frame': coin['time_frame'],
       'percent': percent,
       'seconds': time.seconds,
       'status': operation.operation_type.name,
   }
   return collection.update_one({'_id': coin['_id']}, {"$set": EMA}, upsert=False)


def dropCollection():
   collection = getConnection()
   collection.drop()
