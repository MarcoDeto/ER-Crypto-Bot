import string
from pymongo import MongoClient
import requests 
import numpy as np 
import time
import os
import talib #libreria ta-lib per vari calcoli relativi a indicatori finanziari e tecnici
from binance.client import Client  #importing client 
from config import api_key , api_secret, INTERVAL, SHORT_EMA , LONG_EMA 
from EMA import EMA
from Symbol import Symbol
from Enums import Operation
from Enums import Cross

client = Client(api_key, api_secret)

#Imposto le coin da controllare
SYMBOLS = [
    "BATUSDT",
    "APEUSDT",
    "CELOUSDT",
    "SOLUSDT",
    "LUNABUSD",
    "DOGEUSDT",
    "VETUSDT"
]

Symbols = {}
listacoin = {}

for i in SYMBOLS:
    listacoin[i] = False

def get_database():
    from pymongo import MongoClient
    import pymongo

    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = "mongodb+srv://dev:ManTyres@mantyres.fwdxdp6.mongodb.net/ManTyres"

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    from pymongo import MongoClient
    client = MongoClient(CONNECTION_STRING)

    # Create the database for our example (we will use the same database throughout the tutorial
    return client['EMAs']

def insertEMA(coin, price, operation, cross, ema_short, ema_long, last_ema_short, last_ema_long):

    ema = EMA(coin, price, operation, cross, ema_short, ema_long, last_ema_short, last_ema_long)
    mongoDB = get_database()
    Collection = mongoDB["EMAs"]
    Collection.insert_one(ema)

def checkCoin(coin: Symbol, cross: Cross):

    if (coin.isBuyAllowed == True and coin.isSellAllowed == True):
        if (cross == Cross.LONG): listacoin[coin].isBuyAllowed = False
        if (cross == Cross.SHORT): listacoin[coin].isSellAllowed = False
        return Operation.OPEN
    if (cross == Cross.LONG and coin.isBuyAllowed == False):
        listacoin[coin].isBuyAllowed = True
        return Operation.CLOSE
    if (cross == Cross.SHORT and coin.isSellAllowed == False):
        listacoin[coin].isSellAllowed = True
        return Operation.CLOSE
    else:
        return False
    # OPEN_OPERATION = cross.name+'-'+Operation.OPEN.name
    # CLOSE_OPERATION = cross.name+'-'+Operation.CLOSE.name
    # coinOperation: string = listacoin.get(coin)
    # splitted = coinOperation.split('-')
    # coin_cross = {}
    # operation = {}
    # if (splitted.lenght > 1):
    #     coin_cross = splitted[0]
    #     operation = splitted[1]
    # if (coinOperation == False or operation == Operation.CLOSE):
    #     listacoin[coin] = OPEN_OPERATION
    #     return Operation.OPEN
    # if (operation == Operation.OPEN and coin_cross != cross):
    #     listacoin[coin] = CLOSE_OPERATION
    #     return Operation.CLOSE
    # else:
    #     return False


# otteniamo i dati di klines da elaborare
def get_klines(symbol: Symbol):
    data = client.get_klines(symbol=symbol.symbol,interval=INTERVAL,limit=300)
    # più dati significa più precisione ma a un compromesso tra velocità e tempo
    return_data = []
    # prendendo i dati di chiusura per ogni kline
    for each in data:
        return_data.append(float(each[4])) # 4 è l'indice dei dati di chiusura in ogni kline 
    return np.array(return_data) # ritornando come array numpy per una migliore precisione e prestazioni
 
def Long(coin, ema_short, ema_long, last_ema_short, last_ema_long):
    
    if (ema_short > ema_long and last_ema_short < last_ema_long):
        
        operation = checkCoin(coin, Cross.LONG)
        if (operation == False) :
            return
        insertEMA(coin, price_coin, operation, Cross.LONG, ema_short, ema_long, last_ema_short, last_ema_long)
        print(coin + " "+ str(SHORT_EMA) + " Sopra "+str(LONG_EMA))
        print(coin, "è arrivata l'allerta in long acquisto")
        Cprz = client.get_symbol_ticker(symbol=coin)
        price_coin = Cprz["price"]
        #save_coin = open("/home/fabry/progetti/bot/" + coin + ".txt", "a")
        #save_coin.writelines(" Entrata " + coin + " " + price_coin + "\n")
        #save_coin.writelines("-------------------------------------------------" + "\n")
        #save_coin.close()
        
def Short(coin, ema_short, ema_long, last_ema_short, last_ema_long):
    
    if (ema_short < ema_long and last_ema_short > last_ema_long):

        operation = checkCoin(coin, Cross.SHORT)
        if (operation == False) :
            return
        insertEMA(coin, price_coin, operation, Cross.SHORT, ema_short, ema_long, last_ema_short, last_ema_long)
        print(coin + " "+ str(LONG_EMA) + " Sopra "+str(SHORT_EMA))
        print(coin, "è arrivata l'allerta in short vendita")
        Cprz = client.get_symbol_ticker(symbol=coin)
        price_coin = Cprz["price"]
        #save_coin = open("/home/fabry/progetti/bot/" + coin + ".txt", "a")
        #save_coin.writelines(" Uscita " + coin + " " + price_coin + "\n")
        #save_coin.writelines("-------------------------------------------------" + "\n")
        #save_coin.close()
        
# punto di ingresso per il file
def main(): 

    Symbols = client.get_all_isolated_margin_symbols()
    listacoin = Symbols
    
    buy = False #significa che dobbiamo ancora comprare e non abbiamo comprato
    sell = True #non abbiamo venduto, ma se vuoi acquistare prima, impostalo su True
    acquisto = False

    # creando un ciclo infinito che continua a verificare la condizione
    while True:
        #passando in rassegna ogni coin
        for coin in Symbols:
            data = get_klines(coin)
            ema_short = talib.EMA(data,int(SHORT_EMA))
            ema_long = talib.EMA(data,int(LONG_EMA))
            last_ema_short  = ema_short[-2]
            last_ema_long = ema_long[-2]
            ema_short = ema_short[-1]
            ema_long = ema_long[-1]
            # condizioni per gli avvisi incrocio ema long
            Long(coin, ema_short, ema_long, last_ema_short, last_ema_long)      	
            # condizioni per gli avvisi incrocio ema short
            Short(coin, ema_short, ema_long, last_ema_short, last_ema_long)
            	
        time.sleep(0.5)
            
if __name__ == "__main__":
    main()