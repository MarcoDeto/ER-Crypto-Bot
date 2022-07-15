import asyncio
from datetime import datetime
from models.enums import CycleType
from services.emas import checkCycle
from services.settings import getTimeframesCycle
from services.telegram import *
from services.binance import get_klines, getStartCandle, getSymbols
from services.coins import isToSkip


async def cycleLoop(cycle, my_channel):

    START = None
    print('\nSTART')
    print(cycle)
    print(datetime.now())
    Symbols = getSymbols()
    coin = Symbols[0]
    symbol = coin['symbol']
    if (isToSkip(symbol)):
        return
    
    while START == None:
        START = input('INSERT NUMBER OF CANDLES TO BACK: ')
        try:
            START = int(START)
        except:
            START = None

    TIME_FRAME = getTimeframesCycle(cycle)
    START_CANDLE = getStartCandle(symbol, TIME_FRAME, START)
    START = START_CANDLE

    delay = getDelay(cycle)
    while True:
        await asyncio.sleep(delay)
        print(datetime.now())
        print(cycle.name + '\n')
        
        candles = get_klines(symbol, TIME_FRAME)
        START_CANDLE = await checkCycle(START, candles, coin, cycle, my_channel)
        if (START_CANDLE != START):
            START = START_CANDLE
            continue
        


        

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


async def main():

    await initTelegram()
    my_channel = await getChannel()
    # Schedule three calls *concurrently*:
    L = await asyncio.gather(
        cycleLoop(CycleType.Day, my_channel),
    )
    print(L)

asyncio.run(main())