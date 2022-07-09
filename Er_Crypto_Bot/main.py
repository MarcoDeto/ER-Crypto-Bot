from datetime import datetime
from services.mongoDB import dropCollection
from config import INTERVALS
from services.binance import getSymbols, get_historical_klines
from services.coins import isToSkip
from services.emas import checkEMAs

def main():
    #dropCollection()
    for interval in INTERVALS:
        intervaLoop(interval)


def intervaLoop(interval):
    
    print('\nSTART')
    print(interval)
    print(datetime.now())
    Symbols = getSymbols()
    coin = Symbols[0]
    symbol = coin['symbol']
    if (isToSkip(symbol)):
        return
        
    data = get_historical_klines(symbol, interval)
    klines = len(data)
    if (klines < 300):
        print('There are less than 300 candles! Not accurate calculation!')
        return
    candles = data[0:300]
    
    while True:
        checkEMAs(candles, coin, interval)
        if (len(candles) != klines):
            candles.append(data[len(candles)])
        else: 
            return


def check_coount(interval, index):
    if (index > 1200):
        print('\nEND\n')
        print(interval)
        print(datetime.now())


if __name__ == '__main__':
    try:
        main()
    except Exception as f:
        print('main error: ', f)


