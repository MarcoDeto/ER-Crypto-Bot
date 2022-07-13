import string
import numpy as np  # pip3 install numpy
from binance.client import Client  # pip3 install python-binance
from binance import BinanceSocketManager
from config import *
from models.operation import Operation

client = Client(api_key, api_secret)
bm = BinanceSocketManager(client)


async def WebSocket(symbol):

    # start any sockets here, i.e a trade socket
    ts = bm.trade_socket(symbol)
    # then start receiving messages
    async with ts as tscm:
        while True:
            res = await tscm.recv()
            print(res)
            for interval in INTERVALS:
                print(interval)
                data = get_klines(symbol, interval)

    await client.close_connection()


def get_historical_klines(symbol: Operation, interval: string, startDate, endDate):

    startDate = startDate.strftime("%d %B, %Y")
    endDate = endDate.strftime("%d %B, %Y")

    data = client.get_historical_klines(symbol=symbol, interval=interval, start_str=startDate, end_str=endDate)

    return data


# otteniamo i dati di klines da elaborare
def get_klines(symbol: Operation, interval: string):

    data = client.get_klines(symbol=symbol, interval=interval, limit=300)
    return data


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


def getPrice(symbol):

    Cprz = client.get_symbol_ticker(symbol=symbol)
    return Cprz['price']


def diffPercent(Xi, Xf):
    #[(Xf - Xi)/ Xi ] x 100 %
    if (Xf > Xi):
        return ((float(Xf) - float(Xi)) / float(Xi)) * 100
    if (Xi > Xf):
        return ((float(Xi) - float(Xf)) / float(Xf)) * 100
    else:
        return 0


def diffTime(open, close):
    return close - open

