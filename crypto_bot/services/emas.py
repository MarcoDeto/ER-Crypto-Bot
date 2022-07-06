from models.Enums import CrossType
from services.coins import checkCoin
from services.mongoDB import insertEMA
from binance.client import Client  #pip3 install python-binance
from config import api_key, api_secret 

client = Client(api_key, api_secret)

def Long(coin, ema_short, ema_long, last_ema_short, last_ema_long):
    
    if (ema_short > ema_long and last_ema_short < last_ema_long):
        
        operation = checkCoin(coin, CrossType.LONG)
        if (operation == False): return

        Cprz = client.get_symbol_ticker(symbol=coin['symbol'])
        price_coin = Cprz['price']
        insertEMA(price_coin, operation, CrossType.LONG)
        

def Short(coin, ema_short, ema_long, last_ema_short, last_ema_long):
    
    if (ema_short < ema_long and last_ema_short > last_ema_long):

        operation = checkCoin(coin, CrossType.SHORT)
        if (operation == False): return

        Cprz = client.get_symbol_ticker(symbol=coin['symbol'])
        price_coin = Cprz['price']
        insertEMA(price_coin, operation, CrossType.SHORT)
        