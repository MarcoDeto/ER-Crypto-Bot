#Imposto le coin da controllare
from models.Enums import *
from models.Operation import Operation
from models.Symbol import Symbol
from services.mongoDB import getEMA

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
   
def find(val, list):
   for x in list:
      test = x['symbol']
      if (test and test != val):
         continue
      return x

def checkCoin(coin, cross: CrossType):

   result = getEMA(coin['symbol'])
   if (result):
      coin = result

   newcoin = Symbol(
      coin['symbol'], coin['base'], coin['quote'],
      coin['isMarginTrade'], True, True, 
      getOperationNumber(coin, OperationType.CLOSE)
   )
   if (cross == CrossType.LONG):
      openLong = Symbol(
         coin['symbol'], coin['base'], coin['quote'],
         coin['isMarginTrade'], False, True, 
         getOperationNumber(coin, OperationType.OPEN)
      )
      if (coin['isBuyAllowed'] == True and coin['isSellAllowed'] == True):
         return Operation(openLong, OperationType.OPEN)
      if (coin['isBuyAllowed'] == False):
         return Operation(newcoin, OperationType.CLOSE)

   if (cross == CrossType.SHORT):
      openShort = Symbol(
         coin['symbol'], coin['base'], coin['quote'],
         coin['isMarginTrade'], True, False, 
         getOperationNumber(coin, OperationType.OPEN)
      )
      if (coin['isBuyAllowed'] == True and coin['isSellAllowed'] == True):
         return Operation(openShort, OperationType.OPEN)
      if (coin['isSellAllowed'] == False):
         return Operation(newcoin, OperationType.CLOSE)

   return False

def getOperationNumber(lastDBRow, operationType):
   if hasattr(lastDBRow, 'operation_number'):
      operationNUmber = lastDBRow.operation_number
      print(operationNUmber)
   else:
      return 0