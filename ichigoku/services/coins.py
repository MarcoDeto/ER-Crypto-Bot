from bson import ObjectId
from services.database.mongoDB import getOperationNumber
from models.enums import *
from models.operation import Operation

SKIP_SYMBOLS = [
    'KP3RBTC',
    'BAKEBTC',
    'QNTBUSD',
    'ASTRUSDT',
    'ALGOBTC'
]

def isToSkip(symbol):
   if symbol in SKIP_SYMBOLS:
      return True
   return False


def checkOperation(coin, cross, newOperation):

   if (cross == CrossType.LONG):
      return openLongOperation(newOperation, coin)

   if (cross == CrossType.SHORT):
      return openShortOperation(newOperation, coin)

   return False


def createOperation(coin, cross, interval):
   _id = ObjectId()
   return Operation(
       _id, coin['symbol'], coin['base'], 
       coin['quote'], coin['isMarginTrade'], 
       True, True, 0, cross, Status.OPEN, interval
   )


def updateOperation(newOperation: Operation, coin, interval):
   newOperation.operation_number = getOperationNumber(coin, interval)
   newOperation.operation_type = Status.OPEN
   if (newOperation.cross == CrossType.LONG):
      newOperation.isBuyAllowed = False
   if (newOperation.cross == CrossType.SHORT):
      newOperation.isSellAllowed = False
   return newOperation


def openLongOperation(newcoin: Operation, coin):
   interval = newcoin.time_frame
   newcoin.operation_number = getOperationNumber(coin, interval)
   newcoin.isBuyAllowed = False
   return newcoin


def openShortOperation(newcoin: Operation, coin):
   interval = newcoin.time_frame
   newcoin.operation_number = getOperationNumber(coin, interval)
   newcoin.isSellAllowed = False
   return newcoin


def closeOperation(newcoin: Operation, coin):
   interval = newcoin.time_frame
   newcoin.operation_number = getOperationNumber(coin, interval)
   newcoin.operation_type = Status.CLOSE
   return newcoin
