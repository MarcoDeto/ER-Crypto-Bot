import time
import asyncio
from binance.client import Client
from config import *

from models.ichimoku import Ichimoku
server_time = int(round(time.time() * 1000))

exchange_symbols = []


def getTimeDifference():
    client = Client(TEST_BINANCE_API_KEY, TEST_BINANCE_API_SECRET, testnet=False)
    data = client.futures_klines(symbol='BTCUSDT', interval='1m', limit=1)
    server_time = int(round(time.time() * 1000))
    binance_time = (data[0][0])
    return (server_time - binance_time)


def getActionType(self,time:int) -> chr:
        if(int(time // 86400000) != self.detect1d):

            self.detect1d = int(time // 86400000)
            return 'd'

        if(int(time//14400000) != self.detect4h):
            self.detect4h = int(time // 14400000)
            return 'q'

        if (int(time// 3600000) != self.detect1h):
            print(str(int(time// 3600000)) + "    "+ str(self.detect1h))
            self.detect1h = int(time // 3600000)
            return 'h'
        return 'n'


#initialize exchange symbols here
def initialize(symbols):
    oneHour = {}
    fourHours = {}
    oneDay = {}
    for i in range(len(symbols)):
        currentSymbol = symbols[i]
        oneHour[currentSymbol] = \
            Ichimoku(currentSymbol,'binance', ICHIMOKU_PARAMS, 'h')
        fourHours[currentSymbol] = \
            Ichimoku(currentSymbol, 'binance', ICHIMOKU_PARAMS, 'q')
        oneDay[currentSymbol] = \
            Ichimoku(currentSymbol, 'binance', ICHIMOKU_PARAMS, 'd')
    return (oneHour,fourHours,oneDay)


async def get_klines(symbol, interval, maxparam):
    client = Client(TEST_BINANCE_API_KEY, TEST_BINANCE_API_SECRET, testnet=False)
    data = client.futures_klines(symbol=symbol, interval=interval, limit=maxparam)
    return data

async def runKlines(interval, maxparam, symbols):
    tasks = []
    for symbol in symbols:
        currentSymbol = symbol
        task = asyncio.ensure_future(get_klines(currentSymbol, interval, maxparam))
        tasks.append(task)

    responses = await asyncio.gather(*tasks)
    return responses

def getData(interval, symbols):
    maxparam = max(ICHIMOKU_PARAMS)
    binanceinterval = str
    if (interval == 'h'):
        binanceinterval = '1h'
    if (interval == 'q'):
        binanceinterval = '4h'
    if (interval == 'd'):
        binanceinterval = '1d'
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(runKlines(binanceinterval,maxparam, symbols))
    responses = loop.run_until_complete(future)
    returndict = {}
    for i in range(len(symbols)):
        returndict[symbols[i]] = list(responses[i])
    return returndict


def getCurrentPrice(symbols):
    client = Client(BINANCE_API_KEY, BINANCE_API_SECRET)
    result = []
    for symbol in symbols:
        Cprz = client.futures_symbol_ticker(symbol=symbol)
        toadd = Symbol(symbol, Cprz['price'])
        result.append(toadd)

    return result


class Symbol:
    def __init__(self, symbol, price):
        self.symbol = symbol
        self.price = price