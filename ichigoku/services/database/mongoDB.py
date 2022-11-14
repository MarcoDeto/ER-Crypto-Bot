
from bson import ObjectId  # pip3 install pymongo
from pymongo import MongoClient  # pip3 install 'pymongo[srv]'

import pymongo
from services.settings import *
from models.operation import *
from services.database.query import *
from services.exchange.bybit import *
from services.messages.tradingview import *
from services.messages.messages import *
from services.messages.telegram import *
from config import CONNECTION_STRING
from models.operation import Operation
from services.exchange.binance import *


client = MongoClient(CONNECTION_STRING)
mongoDB = client['Er_Crypto_Bot']
collection = mongoDB['Test']


def getIchimokus():

   item_details = collection.find()
   result = []
   for item in item_details:
      result.append(item)
   return result


def getIchimokuDB(coin, cross, interval):

   query = get_ichimoku(coin, interval, cross)

   item_details = collection.find(query).sort('open_date', pymongo.DESCENDING)
   result = {}
   i = 0
   for item in item_details:
      result[i] = item
      i = i+1
   if (len(result) > 0):
      return result[0]
   return coin


def get_open_operations_DB(coin):
   
   query = get_open_operations(coin)

   item_details = collection.find(query).sort('open_date', pymongo.DESCENDING)
   result = {}
   i = 0
   for item in item_details:
      result[i] = item
      i = i+1
   if (len(result) > 0):
      return result
   return None


def get_operation_DB(coin, cross, interval):
   operationDB = getIchimokuDB(coin, cross, interval)
   if (operationDB):
       return operationDB
   return coin


def getOperationNumber(coin, interval):
   query = get_operation_number(coin, interval)
   result = collection.count_documents(query)
   return result + 1


def check_if_open(coin, cross, interval):

   query = get_open_ichimoku(coin, cross, interval)
   item_details = collection.find(query).sort('open_date', pymongo.ASCENDING)
   result = []
   for item in item_details:
      result.append(item)
   if (len(result) > 0):
      return result[0]
   return None


def insert_ichiGoku(ichimoku):
   print('INSERT\n')
   collection.insert_one(ichimoku)


def get_trailing_stops(open_operations, price, senkou_span_A, senkou_span_B):
   result = []
   # if (price < kijun_sen):
   #    query = get_long_trailing_stop(symbol, interval, price)
   #    item_details = collection.find(query)

   # elif (price > kijun_sen):
   #    query = get_short_trailing_stop(symbol, interval, price)
   #    item_details = collection.find(query)

   # if item_details != None:
   #    for item in item_details:
   #       result.append(item)
         
   if open_operations == None or len(open_operations) == 0:
      return None
   i = 0
   #50% con kingunsen e 50% con senkou_span_B
   for operation in open_operations:

      if open_operations[i]['cross'] == 'SHORT' and price > senkou_span_B and senkou_span_B > senkou_span_A:
         result.append(open_operations[i])
      if open_operations[i]['cross'] == 'LONG' and price < senkou_span_B and senkou_span_A < senkou_span_B:
         result.append(open_operations[i])
      i = i + 1

   return result


def get_stop_losses(open_operations, price, senkou_span_A, senkou_span_B):
   result = []
   # query = get_long_stop_loss(symbol, price)
   # item_details = collection.find(query)
   # for item in item_details:
   #    result.append(item)

   # query = get_short_stop_loss(symbol, price)
   # item_details = collection.find(query)
   # for item in item_details:
   #    result.append(item)
   if open_operations == None or len(open_operations) == 0:
      return None
   i = 0
   for operation in open_operations:
      
      if open_operations[i]['cross'] == 'SHORT' and price > senkou_span_A and senkou_span_A > senkou_span_B:
         result.append(open_operations[i])
      if open_operations[i]['cross'] == 'LONG' and price < senkou_span_A and senkou_span_A < senkou_span_B:
         result.append(open_operations[i])
      i = i + 1

   return result


def get_take_profits(open_operations, price, kijun_sen, senkou_span_A, senkou_span_B):
   
   result = []
   # query = get_long_take_profits(symbol, price)
   # item_details = collection.find(query)
   # for item in item_details:
   #    result.append(item)

   # query = get_short_take_profits(symbol, price)
   # item_details = collection.find(query)
   # for item in item_details:
   #    result.append(item)

   i = 0
   for operation in open_operations:
      if open_operations[i]['cross'] == 'SHORT' and price > kijun_sen and senkou_span_B > senkou_span_A:
         result.append(open_operations[i])
      if open_operations[i]['cross'] == 'LONG' and price < kijun_sen and senkou_span_A < senkou_span_B:
         result.append(open_operations[i])
      i = i + 1

         
   return result


def get_double_take_profits(symbol, cross, interval):
   result = []
   query = get_open_ichimoku(symbol, cross, interval)
   item_details = collection.find(query)
   for item in item_details:
      result.append(item)

   return result


def update_ichiGoku(ichimoku):
   collection.update_one({'_id': ichimoku['_id']}, {'$set': ichimoku}, upsert=False)


def dropCollection():
   collection.drop()
