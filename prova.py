#from binance import Client
from binance.client import Client

from binance import BinanceSocketManager
from binance.exceptions import BinanceAPIException, BinanceOrderException
from binance.enums import *
#from twisted.internet import reactor
from config import api_key , api_secret

client = Client(api_key, api_secret)
client.ping()
info = client.get_exchange_info()
#print(info)
status = client.get_system_status()
print(status)
#prices = client.get_all_tickers()
#print(prices)
info = client.get_account()
balance = info['balances']
for b in balance:
  if float(b['free'])>0:
    print('{}: {}'.format(b['asset'], b['free']))
    
#Rilevo il prezzo della coin
Cprz = client.get_symbol_ticker(symbol='CELOUSDT')
print(Cprz)
celo = Cprz["price"]
print(celo)

#tickers = client.get_ticker()
#print(tickers)
scrivi = open("/home/fabry/progetti/bot/test.txt", "a")
scrivi.write("Entrata - " + " CELOUSDT  = " + celo + "\n")
scrivi.close()
