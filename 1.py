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

#SYMBOLS = []
# otteniamo i dati di klines da elaborare
def get_klines(symbol):
    data = client.get_klines(symbol=symbol,interval=INTERVAL,limit=300)
    # piu' dati significa piu' precisione ma a un compromesso tra velocita' e tempo
    return_data = []
    # prendendo i dati di chiusura per ogni kline
    for each in data:
        return_data.append(float(each[4])) # 4 e' l'indice dei dati di chiusura in ogni kline 
    return np.array(return_data) # ritornando come array numpy per una migliore precisione e prestazioni

# punto di ingresso per il file
def main(): 
    
    buy = False #significa che dobbiamo ancora comprare e non abbiamo comprato
    sell = True #non abbiamo venduto, ma se vuoi acquistare prima, impostalo su True
    acquisto = False
    listacoin = {}
    for i in SYMBOLS:
    	listacoin[i] = 'False'
    # creando un ciclo infinito che continua a verificare la condizione
    while True:
        #passando in rassegna ogni moneta 
        for each in SYMBOLS:
            data = get_klines(each)
            ema_short = talib.EMA(data,int(SHORT_EMA))
            ema_long = talib.EMA(data,int(LONG_EMA))
            
            last_ema_short  = ema_short[-2]
            last_ema_long = ema_long[-2]

            ema_short = ema_short[-1]
            ema_long = ema_long[-1]
             
            
            # condizioni per gli avvisi incrocio ema long
            if(ema_short > ema_long and last_ema_short < last_ema_long):
            	message  = each + " "+ str(SHORT_EMA) + " Sopra "+str(LONG_EMA);
            	if listacoin.get(each) == 'False' :
            	
            	    #Rilevo il prezzo della coin
			return
		return
	        
            	
            time.sleep(0.5);
            
# chiaman la funzione
if __name__ == "__main__":
    main()
