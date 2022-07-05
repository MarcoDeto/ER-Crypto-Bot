import requests 
import numpy as np 
import time
import os
import talib #libreria ta-lib per vari calcoli relativi a indicatori finanziari e tecnici
from binance.client import Client  #importing client 
from config import api_key , api_secret, INTERVAL, SHORT_EMA , LONG_EMA 
from models.Symbol import Symbol
from models.Enums import *
from services.coins import *
from services.mongoDB import *

client = Client(api_key, api_secret)

# otteniamo i dati di klines da elaborare
def get_klines(symbol: Symbol):
    data = client.get_klines(symbol=symbol,interval=INTERVAL,limit=300)
    # più dati significa più precisione ma a un compromesso tra velocità e tempo
    return_data = []
    # prendendo i dati di chiusura per ogni kline
    for each in data:
        return_data.append(float(each[4])) # 4 è l'indice dei dati di chiusura in ogni kline 
    return np.array(return_data) # ritornando come array numpy per una migliore precisione e prestazioni


def Long(symbols, coin, ema_short, ema_long, last_ema_short, last_ema_long):
    
    if (ema_short > ema_long and last_ema_short < last_ema_long):
        
        operation = checkCoin(symbols, coin, CrossType.LONG)
        if (operation == False): return

        Cprz = client.get_symbol_ticker(symbol=coin['symbol'])
        price_coin = Cprz['price']
        insertEMA(price_coin, operation, CrossType.LONG, ema_short, ema_long, last_ema_short, last_ema_long)
        

def Short(symbols, coin, ema_short, ema_long, last_ema_short, last_ema_long):
    
    if (ema_short < ema_long and last_ema_short > last_ema_long):

        operation = checkCoin(symbols, coin, CrossType.SHORT)
        if (operation == False): return

        Cprz = client.get_symbol_ticker(symbol=coin['symbol'])
        price_coin = Cprz['price']
        insertEMA(price_coin, operation, CrossType.SHORT, ema_short, ema_long, last_ema_short, last_ema_long)
        

# punto di ingresso per il file
def main(): 
    
    coin_list = client.get_all_isolated_margin_symbols()
    filtered = filter(lambda coin: coin['quote'] == 'USDT' or coin['quote'] == 'BTC', coin_list)
    Symbols = []
    i = 0
    for item in filtered:
        Symbols.append(item)

    # ciclo infinito
    while True:
        
        for coin in Symbols:

            symbol = coin['symbol']
            # skipper
            if (isToSkip(symbol)): 
                continue
            
            data = get_klines(symbol)
            ema_short = talib.EMA(data,int(SHORT_EMA))
            ema_long = talib.EMA(data,int(LONG_EMA))
            last_ema_short  = ema_short[-2]
            last_ema_long = ema_long[-2]
            ema_short = ema_short[-1]
            ema_long = ema_long[-1]
            # condizioni per gli avvisi incrocio ema long
            Long(Symbols, coin, ema_short, ema_long, last_ema_short, last_ema_long)      	
            # condizioni per gli avvisi incrocio ema short
            Short(Symbols, coin, ema_short, ema_long, last_ema_short, last_ema_long)
            	
        time.sleep(0.5)
            
if __name__ == '__main__':
    main()