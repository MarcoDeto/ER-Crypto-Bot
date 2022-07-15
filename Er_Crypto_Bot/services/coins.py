from bson import ObjectId
from services.mongoDB import getOperationNumber
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
      if (coin['isBuyAllowed'] == True and coin['isSellAllowed'] == True):
         return openLongOperation(newOperation, coin)
      if (coin['isSellAllowed'] == False):
         return closeOperation(newOperation, coin)

   if (cross == CrossType.SHORT):
      if (coin['isBuyAllowed'] == True and coin['isSellAllowed'] == True):
         return openShortOperation(newOperation, coin)
      if (coin['isBuyAllowed'] == False):
         return closeOperation(newOperation, coin)

   return False


def createOperation(coin, cross, main_ema, second_ema, interval):
   _id = ObjectId()
   return Operation(
       _id, coin['symbol'], coin['base'], coin['quote'],
       coin['isMarginTrade'], True, True, 0, cross,
       Status.OPEN, main_ema, second_ema, interval
   )


def updateOperation(newOperation: Operation, coin, main_ema, second_ema, interval):
   newOperation.operation_number = getOperationNumber(
       coin, main_ema, second_ema, interval
   )
   newOperation.operation_type = Status.OPEN
   if (newOperation.cross == CrossType.LONG):
      newOperation.isBuyAllowed = False
   if (newOperation.cross == CrossType.SHORT):
      newOperation.isSellAllowed = False
   return newOperation


def openLongOperation(newcoin: Operation, coin):
   second_ema = newcoin.ema_second
   main_ema = newcoin.ema_main
   interval = newcoin.time_frame
   newcoin.operation_number = getOperationNumber(
       coin, main_ema, second_ema, interval
   )
   newcoin.isBuyAllowed = False
   return newcoin


def openShortOperation(newcoin: Operation, coin):
   second_ema = newcoin.ema_second
   main_ema = newcoin.ema_main
   interval = newcoin.time_frame
   newcoin.operation_number = getOperationNumber(
       coin, main_ema, second_ema, interval
   )
   newcoin.isSellAllowed = False
   return newcoin


def closeOperation(newcoin: Operation, coin):
   second_ema = newcoin.ema_second
   main_ema = newcoin.ema_main
   interval = newcoin.time_frame
   newcoin.operation_number = getOperationNumber(
       coin, main_ema, second_ema, interval
   )
   newcoin.operation_type = Status.CLOSE
   return newcoin


def OLDgetOperationNumber(lastDBRow: Operation, operationType, main_ema, second_ema, interval):
   try:
      if (operationType == Status.CLOSE and interval == lastDBRow['time_frame'] and
         second_ema == lastDBRow['ema_second'] and main_ema == lastDBRow['ema_main'] ):
         return lastDBRow['operation_number']
      else:
         return lastDBRow['operation_number'] + 1
   except Exception as error:
      print('excetion cathed, returned 0')
      return 0