import time
import asyncio
from binance.client import Client
from config import *
from models.ichimoku import *

client = Client(BINANCE_API_KEY, BINANCE_API_SECRET, testnet=False)

def getSymbols():
    coin_list = client.get_all_isolated_margin_symbols()
    filtered = filter(
        lambda coin: coin['quote'] == 'USDT' or coin['quote'] == 'BTC', coin_list)
    Symbols = []

    if (len(SYMBOLS) > 0):
        filtered = filter(
            lambda coin: coin['base'] == SYMBOLS[0] and coin['quote'] == 'USDT', coin_list)
    i = 0
    for item in filtered:
        if (i > 49):
            return Symbols
        Symbols.append(item)
        i = i + 1

    return Symbols


def getSymbol(symbol):
    coin_list = client.get_all_isolated_margin_symbols()
    filtered = filter(
        lambda coin: coin['quote'] == 'USDT' or coin['quote'] == 'BTC', coin_list)

    filtered = filter(lambda coin: coin['symbol'] == symbol, coin_list)
    return filtered[0]


def getTimeDifference():
    data = client.futures_klines(symbol='BTCUSDT', interval='1m', limit=1)
    server_time = int(round(time.time() * 1000))
    binance_time = (data[0][0])
    return (server_time - binance_time)


async def get_klines(symbol, interval, maxparam):
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
    ichimoku_params = getIchimokuParams(interval)
    maxparam = max(ichimoku_params)
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(runKlines(interval, maxparam, symbols))
    responses = loop.run_until_complete(future)
    returndict = {}
    for i in range(len(symbols)):
        returndict[symbols[i]] = list(responses[i])
    return returndict


def getCurrentPrices(symbols):
    result = []
    for symbol in symbols:
        Cprz = client.futures_symbol_ticker(symbol=symbol)
        toadd = Symbol(symbol, Cprz['price'])
        result.append(toadd)

    return result

def getPrice(symbol):
    Cprz = client.futures_symbol_ticker(symbol=symbol)
    return Cprz['price']

def open_order(symbol, side, quantity):
    return None
    # client = Client(TEST_BINANCE_API_KEY, TEST_BINANCE_API_SECRET, testnet=True)
    # data = client.futures_create_order(symbol=symbol,type="MARKET",side=side,quantity=1500,)
    # client.futures_create_order(symbol=symbol,type="LIMIT",timeInForce="GTC",side="SELL",price=sellPrice,quantity=quantity)
    # return data

class Symbol:
    def __init__(self, symbol, price):
        self.symbol = symbol
        self.price = price