import asyncio
from datetime import datetime
from services.messages.telegram import *
from services.exchange.binance import get_klines, getSymbols
from services.coins import isToSkip
from services.emas import checkEMAs

async def intervaLoop(interval, telegram):
    
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
        await checkEMAs(candles, coin, interval, telegram)


def getDelay(time_frame):
    match (time_frame):
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


async def main():

    await initTelegram()
    telegram = await getChannel()
    # Schedule three calls *concurrently*:
    L = await asyncio.gather(
        intervaLoop('1m', telegram),
        intervaLoop('3m', telegram),
        intervaLoop('5m', telegram),
        intervaLoop('15m', telegram),
        intervaLoop('30m', telegram),
        intervaLoop('1h', telegram),
        intervaLoop('2h', telegram),
        intervaLoop('4h', telegram),
        intervaLoop('1d', telegram),
    )
    print(L)


try:
    asyncio.run(main())

except Exception as error:
    print('excetion cathed')