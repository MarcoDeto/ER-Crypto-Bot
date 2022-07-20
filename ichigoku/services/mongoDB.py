
from bson import ObjectId  # pip3 install pymongo
from pymongo import MongoClient  # pip3 install "pymongo[srv]"
from datetime import datetime

import pymongo
from services.telegram import *
from config import CONNECTION_STRING
from models.operation import Operation
from services.binance import *
from services.utilities import *

client = MongoClient(CONNECTION_STRING)
mongoDB = client['Er_Crypto_Bot']
collection = mongoDB['IchiGoku']

def getIchimokus():

   item_details = collection.find()
   result = []
   for item in item_details:
      result.append(item)
   return result


def getIchimokuDB(coin, interval):

   query = {
      'symbol': coin['symbol'],
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


def getOperationNumber(coin, interval):
   query = {
      'symbol': coin['symbol'],
      'time_frame': interval,
      'close_price': { '$ne': None }
   }
   result = collection.count_documents(query)
   return result + 1


def insertIchiGoku(operation: Operation):
   print('INSERT\n')
   ichimoku = {
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
       'time_frame': operation.time_frame,
       'percent': 0,
       'seconds': 0,
       'status': 'OPEN',
       'stop_loss': False,
   }
   collection.insert_one(ichimoku)
   #adjust_leverage(operation.symbol)
   #adjust_margintype(operation.symbol)
   if (operation.cross.name == 'LONG'):
      open_order(operation.symbol, 'BUY', 10)
   if (operation.cross.name == 'SHORT'):
      open_order(operation.symbol, 'SELL', 10)


def updateIchiGoku(operation: Operation, coin: Operation, my_channel):
   print('UPDATE')
   open_price = coin['open_price']
   symbol = coin['symbol']
   close_price = float(getPrice(symbol))
   open_date = coin['open_date']
   close_date = datetime.now()
   cross = coin['cross']
   percent = round(diffPercent(open_price, close_price, cross), 2)
   time = diffTime(open_date, close_date)
   ichimoku = {
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
       'time_frame': coin['time_frame'],
       'percent': percent,
       'seconds': time.seconds,
       'status': operation.operation_type.name,
       'stop_loss': False
   }
   collection.update_one({'_id': coin['_id']}, {"$set": ichimoku}, upsert=False)
   #adjust_leverage(symbol)
   #adjust_margintype(symbol)
   if (cross == 'LONG'):
      open_order(symbol, 'SELL', 10)
   if (cross == 'SHORT'):
      open_order(symbol, 'BUY', 10)
   sendMessage(my_channel, symbol, cross, open_date, open_price, close_price, percent, time.seconds, coin['time_frame'])


def checkTakeProfit(symbol, interval, price, kijun_sen, my_channel):
   result = []
   if (float(price) < kijun_sen):
      price_max = (float(price) + (float(price) * 0.95 / 100))
      query = {
         'symbol': symbol,
         "status": 'OPEN', 
         "cross": 'LONG',
         "time_frame": interval,
         'open_price': { '$gt': price_max },
         'close_price': { '$eq': None }
      }
      result = collection.find(query)

   elif (float(price) > kijun_sen):
      price_min = (float(price) - (float(price) * 0.95 / 100))
      query = {
         'symbol': symbol,
         "status": 'OPEN', 
         "cross": 'SHORT', 
         "time_frame": interval,
         'open_price': { '$lt': price_min },
         'close_price': { '$eq': None }
      }
      result = collection.find(query)

   for operation in result:
      print('TAKE PROFIT')
      open_price = operation['open_price']
      open_date = operation['open_date']
      close_date = datetime.now()
      percent = round(diffPercent(open_price, float(price), operation['cross']), 2)
      time = diffTime(open_date, close_date)
      ichimoku = {
         '_id': operation['_id'],
         'symbol': operation['symbol'],
         'base': operation['base'],
         'quote': operation['quote'],
         'isMarginTrade': operation['isMarginTrade'],
         'isBuyAllowed': True,
         'isSellAllowed': True,
         'open_price': open_price,
         'close_price': float(price),
         'open_date': open_date,
         'close_date': close_date,
         'operation_number': operation['operation_number'],
         'cross': operation['cross'],
         'time_frame': operation['time_frame'],
         'percent': percent,
         'seconds': time.seconds,
         'status': 'CLOSE',
         'stop_loss': False
      }
      collection.update_one({'_id': operation['_id']}, {"$set": ichimoku}, upsert=False)
      sendMessage(my_channel, symbol, operation['cross'], open_date, open_price, float(price), percent, time.seconds, operation['time_frame'], stop_loss=False)


def checkStopLoss(symbol, price, my_channel):
   
   price_min = (float(price) - (float(price) * 0.95 / 100))
   query = {
      'symbol': symbol,
      "status": 'OPEN', 
      "cross": 'LONG', 
      'open_price': { '$lt': price_min },
      'close_price': { '$eq': None }
   }
   item_details = collection.find(query)
   result = []
   for item in item_details:
      result.append(item)
   price_max = (float(price) + (float(price) * 0.95 / 100))
   query = {
      'symbol': symbol,
      "status": 'OPEN', 
      "cross": 'SHORT', 
      'open_price': { '$gt': price_max },
      'close_price': { '$eq': None }
   }
   item_details = collection.find(query)
   for item in item_details:
      result.append(item)
   for operation in result:
      print('STOP LOSS')
      open_price = operation['open_price']
      open_date = operation['open_date']
      close_date = datetime.now()
      percent = round(diffPercent(open_price, float(price), operation['cross']), 2)
      time = diffTime(open_date, close_date)
      ichimoku = {
         '_id': operation['_id'],
         'symbol': operation['symbol'],
         'base': operation['base'],
         'quote': operation['quote'],
         'isMarginTrade': operation['isMarginTrade'],
         'isBuyAllowed': True,
         'isSellAllowed': True,
         'open_price': open_price,
         'close_price': float(price),
         'open_date': open_date,
         'close_date': close_date,
         'operation_number': operation['operation_number'],
         'cross': operation['cross'],
         'time_frame': operation['time_frame'],
         'percent': percent,
         'seconds': time.seconds,
         'status': 'CLOSE',
         'stop_loss': True
      }
      collection.update_one({'_id': operation['_id']}, {"$set": ichimoku}, upsert=False)
      sendMessage(my_channel, symbol, operation['cross'], open_date, open_price, float(price), percent, time.seconds, operation['time_frame'], stop_loss=True)



def dropCollection():
   collection.drop()