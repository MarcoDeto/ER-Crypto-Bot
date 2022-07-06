import time
import talib #pip3 install ta-lib
from config import SHORT_EMA , LONG_EMA 
from models.Symbol import Symbol
from services.binance import get_klines, getSymbols
from services.coins import isToSkip
from services.emas import Long, Short


def main(): 
    
    Symbols = getSymbols()

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
            Long(coin, ema_short, ema_long, last_ema_short, last_ema_long)      	
            # condizioni per gli avvisi incrocio ema short
            Short(coin, ema_short, ema_long, last_ema_short, last_ema_long)
            	
        time.sleep(0.5)
            

if __name__ == '__main__':
    main()