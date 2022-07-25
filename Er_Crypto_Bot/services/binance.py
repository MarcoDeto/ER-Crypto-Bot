import string
import numpy as np  # pip3 install numpy
from binance.client import Client  # pip3 install python-binance
from binance import BinanceSocketManager
from config import *
from models.operation import Operation


async def web_socket(symbol):
    client = Client(BINANCE_API_KEY, BINANCE_API_SECRET)
    bm = BinanceSocketManager(client)
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
    client = Client(BINANCE_API_KEY, BINANCE_API_SECRET)
    data = client.get_historical_klines(symbol=symbol, interval=interval, start_str=startDate, end_str=endDate)

    return data


# otteniamo i dati di klines da elaborare
def get_klines(symbol: Operation, interval: string):
    client = Client(TEST_BINANCE_API_KEY, TEST_BINANCE_API_SECRET, testnet=False)
    data = client.futures_klines(symbol=symbol, interval=interval, limit=300)
    return data

def adjust_leverage(symbol):
    client = Client(TEST_BINANCE_API_KEY, TEST_BINANCE_API_SECRET, testnet=True)
    client.futures_change_leverage(symbol=symbol, leverage=10)

def adjust_margintype(symbol):
    client = Client(TEST_BINANCE_API_KEY, TEST_BINANCE_API_SECRET, testnet=True)
    client.futures_change_margin_type(symbol=symbol, marginType='ISOLATED')

def open_order(symbol, side, quantity):
    return None
    # client = Client(TEST_BINANCE_API_KEY, TEST_BINANCE_API_SECRET, testnet=True)
    # data = client.futures_create_order(symbol=symbol,type="MARKET",side=side,quantity=1500,)
    # client.futures_create_order(symbol=symbol,type="LIMIT",timeInForce="GTC",side="SELL",price=sellPrice,quantity=quantity)
    # return data


def get_symbols():
    client = Client(BINANCE_API_KEY, BINANCE_API_SECRET)
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


def get_price(symbol):
    client = Client(BINANCE_API_KEY, BINANCE_API_SECRET)
    Cprz = client.futures_symbol_ticker(symbol=symbol)
    return Cprz['price']


def get_diff_percent(Xi, Xf, cross):
    if (cross == 'LONG'):
        return ((float(Xf) - float(Xi)) / float(Xi)) * 100
    elif (cross == 'SHORT'):
        return ((float(Xi) - float(Xf)) / float(Xf)) * 100
    else:
        return 0


def get_diff_time(open, close):
    return close - open

