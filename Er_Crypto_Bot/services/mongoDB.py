
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
         collection = mongoDB['Cycle Strategy']
         return collection
      except:
         continue


def getEMAs():

   collection = getConnection()
   query = {'close_price': { '$ne': None }}
   item_details = collection.find(query)
   result = []
   for item in item_details:
      result.append(item)
   return result


def dropCollection():
   collection = getConnection()
   collection.drop()
