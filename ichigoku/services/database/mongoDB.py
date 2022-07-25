
from bson import ObjectId  # pip3 install pymongo
from pymongo import MongoClient  # pip3 install "pymongo[srv]"

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
collection = mongoDB['IchiGoku']


def getIchimokus():

   item_details = collection.find()
   result = []
   for item in item_details:
      result.append(item)
   return result


def getIchimokuDB(coin, cross, interval):

   count = collection.count_documents({})
   if (count == 0):
      return None

   query = get_ichimoku(coin, interval, cross)
   count = collection.count_documents(query)
   if (count == 0):
      return coin

   item_details = collection.find(query).sort('open_date', pymongo.DESCENDING)
   result = {}
   i = 0
   for item in item_details:
      result[i] = item
      i = i+1
   if (len(result) > 0):
      return result[0]
   return coin


def getOperationDB(coin, cross, interval):
   operationDB = getIchimokuDB(coin, cross, interval)
   if (operationDB):
       return operationDB
   return coin


def getOperationNumber(coin, interval):
   query = get_operation_number(coin, interval)
   result = collection.count_documents(query)
   return result + 1


def checkIfOpen(coin, cross, interval):
   count = collection.count_documents({})
   if (count == 0):
      return None

   query = get_open_ichimoku(coin, cross, interval)
   count = collection.count_documents(query)
   if (count == 0):
      return None

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


def get_trading_stops(symbol, interval, price, kijun_sen):
   result = []
   if (float(price) < kijun_sen):
      price_max = (float(price) + (float(price) * 0.95 / 100))
      query = get_long_trading_stop(symbol, interval, price_max)
      result = collection.find(query)

   elif (float(price) > kijun_sen):
      price_min = (float(price) - (float(price) * 0.95 / 100))
      query = get_short_trading_stop(symbol, interval, price_min)
      result = collection.find(query)

   return result



def get_stop_losses(symbol, interval, price):
   result = []
   tollerance = get_stop_loss_tollerance(interval)
   price_min = (float(price) - (float(price) * tollerance / 100))
   query = get_long_stop_loss(symbol, price_min)
   item_details = collection.find(query)

   for item in item_details:
      result.append(item)

   price_max = (float(price) + (float(price) * tollerance / 100))
   query = get_short_stop_loss(symbol, price_max)
   item_details = collection.find(query)

   for item in item_details:
      result.append(item)

   return result


def update_ichiGoku(ichimoku):
   collection.update_one({'_id': ichimoku['_id']}, {"$set": ichimoku}, upsert=False)


def get_long_take_profits(symbol, interval):
   result = []
   query = get_long_take_profit(symbol, interval)
   item_details = collection.find(query)
   for item in item_details:
      result.append(item)

   return result


def get_short_take_profits(symbol, interval):
   result = []
   query = get_short_take_profit(symbol, interval)
   item_details = collection.find(query)
   for item in item_details:
      result.append(item)
   
   return result


def dropCollection():
   collection.drop()
