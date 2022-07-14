import asyncio
from datetime import datetime
from services.emas import checkCycle
from services.mongoDB import updateOperations
from services.settings import getTimeframesCycle
from config import CYCLETYPES
from services.binance import get_klines, getSymbols
from services.coins import isToSkip

def main():
    loop = asyncio.get_event_loop()
    for cycle in CYCLETYPES:
        loop.create_task(cycleLoop(cycle))

    loop.run_forever()


def getDelay(time_frame):
    match time_frame:
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
        case '3d':
            return 432
        case _:
            return 1

async def cycleLoop(cycle):
    await updateOperations()
    print('\nSTART')
    print(cycle)
    print(datetime.now())
    Symbols = getSymbols()
    coin = Symbols[0]
    symbol = coin['symbol']
    if (isToSkip(symbol)):
        return
        
    delay = getDelay(cycle)
    while True:
        await asyncio.sleep(delay)
        print(datetime.now())
        print(cycle.name + '\n')
        time_frame = getTimeframesCycle(cycle)
        candles = get_klines(symbol, time_frame)
        await checkCycle(candles, coin, cycle)


if __name__ == '__main__':
    try:
        main()
    except Exception as f:
        print('main error: ', f)