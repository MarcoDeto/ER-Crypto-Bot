
from bson import ObjectId # pip3 install pymongo
from pymongo import MongoClient # pip3 install "pymongo[srv]"
from datetime import datetime
from config import CONNECTION_STRING, INTERVAL, LONG_EMA, SHORT_EMA
from models.Enums import OperationType

def getConnection():
   client = MongoClient(CONNECTION_STRING)
   mongoDB = client['ManTyres']
   collection = mongoDB['EMAs']
   return collection

def getEMAs():

   collection = getConnection()
   item_details = collection.find()
   result = []
   for item in item_details:
      result.append(item)
   return result

def getDistinctEMAs():

   print()

def getEMA(symbol):

   collection = getConnection()
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

def insertEMA(price, operation, cross):

   collection = getConnection()
   operationType = operation.operation
   lastDBRow = operation.coin
   EMA = {
        '_id' : ObjectId(),
        'symbol': lastDBRow.symbol,
        'base': lastDBRow.base,
        'quote': lastDBRow.quote,
        'isMarginTrade': lastDBRow.isBuyAllowed,
        'isBuyAllowed': lastDBRow.isBuyAllowed,
        'isSellAllowed': lastDBRow.isSellAllowed,
        'price': price,
        'operation_number': lastDBRow.operation_number,
        'operation': operationType.name,
        'cross': cross.name,
        'time_frame': INTERVAL,
        'ema_main': SHORT_EMA,
        'ema_second': LONG_EMA,
        'CreateAT': datetime.now()
   }
   return collection.insert_one(EMA)

