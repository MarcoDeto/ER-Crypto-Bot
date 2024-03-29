import asyncio
from datetime import datetime
from config import INTERVALS
from services.binance import get_klines, getSymbols
from services.coins import isToSkip
from services.emas import checkEMAs

def main():
    loop = asyncio.get_event_loop()
    for interval in INTERVALS:
        loop.create_task(intervaLoop(interval))

    loop.run_forever()


def getDelay(interval):
    match interval:
        case '1m':
            return .1
        case '3m':
            return .3
        case '5m':
            return .5
        case '15m':
            return 1.5
        case '30m':
            return 3
        case '45m':
            return 4.5
        case '1h':
            return 6
        case '2h':
            return 12
        case '3h':
            return 18
        case '4h':
            return 24
        case '1d':
            return 144
        case _:
            return 1

async def intervaLoop(interval):
    
    print('\nSTART')
    print(interval)
    print(datetime.now())
    Symbols = getSymbols()
    coin = Symbols[0]
    symbol = coin['symbol']
    if (isToSkip(symbol)):
        return
        
    delay = getDelay(interval)
    while True:
        await asyncio.sleep(delay)
        print(datetime.now())
        print(interval + '\n')
        candles = get_klines(symbol, interval)
        checkEMAs(candles, coin, interval)


if __name__ == '__main__':
    try:
        main()
    except Exception as f:
        print('main error: ', f)