from binance.client import Client  # pip3 install python-binance
import numpy as np  # pip3 install numpy
from config import api_key , api_secret, INTERVAL
from models.Symbol import Symbol

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

def getSymbols():
   coin_list = client.get_all_isolated_margin_symbols()
   filtered = filter(lambda coin: coin['quote'] == 'USDT' or coin['quote'] == 'BTC', coin_list)
   Symbols = []
   i = 0
   for item in filtered:
       Symbols.append(item)
   return Symbols