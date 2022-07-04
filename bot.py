##inizieremo con definendo alcune costanti
import  requests 
import numpy as np 
import time
import os
import talib #libreria talib per vari calcoli relativi a indicatori finanziari e tecnici
from binance.client  import Client  #importing client 
from config import api_key , api_secret, INTERVAL, SHORT_EMA , LONG_EMA 

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

listacoin = {}
for i in SYMBOLS:
    listacoin[i] = 'False'

#SYMBOLS = []
# otteniamo i dati di klines da elaborare
def get_klines(symbol):
    data = client.get_klines(symbol=symbol,interval=INTERVAL,limit=300)
    # più dati significa più precisione ma a un compromesso tra velocità e tempo
    return_data = []
    # prendendo i dati di chiusura per ogni kline
    for each in data:
        return_data.append(float(each[4])) # 4 è l'indice dei dati di chiusura in ogni kline 
    return np.array(return_data) # ritornando come array numpy per una migliore precisione e prestazioni
 
def Long(coin, ema_short, ema_long, last_ema_short, last_ema_long):
    
    if(ema_short > ema_long and last_ema_short < last_ema_long):
        message = coin + " "+ str(SHORT_EMA) + " Sopra "+str(LONG_EMA)
        
        if listacoin.get(coin) == 'True' :
            return
        
        print(message)
        print(coin, "è arrivata l'allerta in long acquisto") 
        Cprz = client.get_symbol_ticker(symbol=coin)
        prezzocoin = Cprz["price"]

        salvacoin = open("/home/fabry/progetti/bot/" + coin + ".txt", "a")
        salvacoin.writelines(" Entrata " + coin + " " + prezzocoin + "\n")
        salvacoin.close()
        listacoin.get[coin] = 'True'
        
def Short(coin, ema_short, ema_long, last_ema_short, last_ema_long):
    
    if(ema_short < ema_long and last_ema_short > last_ema_long):
        message = coin + " "+ str(LONG_EMA) + " Sopra "+str(SHORT_EMA)
        
        if listacoin.get(coin) == 'True' :
            return
        
        print(message)
        print(coin, "è arrivata l'allerta in short vendita") 
        Cprz = client.get_symbol_ticker(symbol=coin)
        prezzocoin = Cprz["price"]

        salvacoin = open("/home/fabry/progetti/bot/" + coin + ".txt", "a")
        salvacoin.writelines(" Uscita " + coin + " " + prezzocoin + "\n")
        salvacoin.writelines("-------------------------------------------------" + "\n")
        salvacoin.close()
        listacoin.get[coin] = 'False'
        
# punto di ingresso per il file
def main(): 
    
    buy = False #significa che dobbiamo ancora comprare e non abbiamo comprato
    sell = True #non abbiamo venduto, ma se vuoi acquistare prima, impostalo su True
    acquisto = False

    # creando un ciclo infinito che continua a verificare la condizione
    while True:
        
        #passando in rassegna ogni moneta 
        for coin in SYMBOLS:
            Long
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
            	
        time.sleep(0.5);
            
# chiaman la funzione
if __name__ == "__main__":
    main()
            
            
            
            
            
            
            
    
    
    
    
    
    
    
    
    
    
    
    
    
