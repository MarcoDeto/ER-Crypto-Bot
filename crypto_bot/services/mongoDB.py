
from bson import ObjectId
from pymongo import MongoClient
from datetime import datetime
from config import INTERVAL, SHORT_EMA , LONG_EMA 

def insertEMA(price, operation, cross, ema_short, ema_long, last_ema_short, last_ema_long):

   CONNECTION_STRING = 'mongodb+srv://dev:ManTyres@mantyres.fwdxdp6.mongodb.net'
   client = MongoClient(CONNECTION_STRING)
   mongoDB = client['ManTyres']
   collection = mongoDB['EMAs']
   operationType = operation.operation
   coin = operation.coin
   EMA = {
        '_id' : ObjectId(),
        'symbol': coin.symbol,
        'base': coin.base,
        'quote': coin.quote,
        'isMarginTrade': coin.isBuyAllowed,
        'isBuyAllowed': coin.isBuyAllowed,
        'isSellAllowed': coin.isSellAllowed,
        'price': price,
        'operation': operationType.name,
        'cross': cross.name,
        'time_frame': INTERVAL,
        'ema_main': SHORT_EMA,
        'ema_second': LONG_EMA,
        'ema_short': ema_short,
        'ema_long': ema_long,
        'last_ema_short': last_ema_short,
        'last_ema_long': last_ema_long,
        'CreateAT': datetime.now()
   }
   return collection.insert_one(EMA)

def getEMAs():

   CONNECTION_STRING = 'mongodb+srv://dev:ManTyres@mantyres.fwdxdp6.mongodb.net'
   client = MongoClient(CONNECTION_STRING)
   mongoDB = client['ManTyres']
   collection = mongoDB['EMAs']
   item_details = collection.find()
   result = {}
   i = 0
   for item in item_details:
      result[i] = item
      i = i+1
   return result

def getEMA(symbol):

   CONNECTION_STRING = 'mongodb+srv://dev:ManTyres@mantyres.fwdxdp6.mongodb.net'
   client = MongoClient(CONNECTION_STRING)
   mongoDB = client['ManTyres']
   collection = mongoDB['EMAs']
   query = {'symbol': symbol}
   item_details = collection.find(query).sort('symbol')
   result = {}
   i = 0
   for item in item_details:
      result[i] = item
      i = i+1
   if (len(result) > 0):
      return result[0]
   return result