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

def checkCoin(symbols, coin, cross: CrossType):

   result = getEMA(coin['symbol'])
   if (result):
      coin = result

   newcoin = Symbol(coin['symbol'], coin['base'], coin['quote'], coin['isMarginTrade'], True, True)

   if (cross == CrossType.LONG):
      openLong = Symbol(coin['symbol'], coin['base'], coin['quote'], coin['isMarginTrade'], False, True)
      if (coin['isBuyAllowed'] == True and coin['isSellAllowed'] == True):
         return Operation(openLong, OperationType.OPEN)
      if (coin['isBuyAllowed'] == False):
         return Operation(newcoin, OperationType.CLOSE)

   if (cross == CrossType.SHORT):
      openShort = Symbol(coin['symbol'], coin['base'], coin['quote'], coin['isMarginTrade'], True, False)
      if (coin['isBuyAllowed'] == True and coin['isSellAllowed'] == True):
         return Operation(openShort, OperationType.OPEN)
      if (coin['isSellAllowed'] == False):
         return Operation(newcoin, OperationType.CLOSE)

   return False