from datetime import datetime
import hmac
import time
from urllib.parse import quote_plus
from pybit import usdt_perpetual, inverse_perpetual
import requests
import urllib3

from config import *


session_unauth = usdt_perpetual.HTTP(endpoint=TEST_BYBIT_BASE_URL)

session_auth = usdt_perpetual.HTTP(
    endpoint=TEST_BYBIT_BASE_URL,
    api_key=TEST_BYBIT_API_KEY,
    api_secret=TEST_BYBIT_API_SECRET
)


def get_bybit_symbols():
    url = TEST_BYBIT_BASE_URL + "/derivatives/v3/public/instruments-info"
    parameters = {
        "category": "linear"
    }
    response = requests.get(url, params=parameters)
    if response.status_code == 200:
        print("sucessfully fetched the data")
        return response.json()['result']['list']
    else:
        print("there's a {response.status_code} error with your request")


def klines(symbol, interval):
    time_frame = get_bybit_interval(interval)
    now = datetime.now()
    timestamp = int(datetime.timestamp(now))
    return session_unauth.query_kline(
        symbol=symbol,
        interval=time_frame,
        limit=200,
        from_time=timestamp - 2000
    )['result']


def mark_price_klines(symbol):
    now = datetime.now()
    timestamp = int(datetime.timestamp(now))
    session_unauth = usdt_perpetual.HTTP(
        endpoint="https://api-testnet.bybit.com"
    )
    return session_unauth.query_mark_price_kline(
        symbol='BTCUSDT',
        interval=1,
        limit=200,
        from_time=timestamp - 2000
    )['result']


def get_bybit_price(symbol):
    klines = mark_price_klines(symbol)
    return klines[-1]['close']


def get_wallet_balance():
    response = session_auth.get_wallet_balance()
    ADA = response['result']['ADA']
    BIT = response['result']['BIT']
    BTC = response['result']['BTC']
    DOT = response['result']['DOT']
    EOS = response['result']['EOS']
    ETH = response['result']['ETH']
    LTC = response['result']['LTC']
    LUNA = response['result']['LUNA']
    MANA = response['result']['MANA']
    SOL = response['result']['SOL']
    USDT = response['result']['USDT']
    XRP = response['result']['XRP']
    return (ADA, BIT, BTC, DOT, EOS, ETH, LTC, LUNA, MANA, SOL, USDT, XRP)


def get_usdt_balance():
    response = session_auth.get_wallet_balance()
    USDT = response['result']['USDT']
    return USDT['available_balance']


def get_order_quantity(symbol):
    usdt = get_usdt_balance()
    usdt_quantity = (usdt * 3) / 100
    price = get_bybit_price(symbol)
    return round(usdt_quantity / price, 3)


def place_order(symbol, side, take_profit, stop_loss, quantity):
    return session_auth.place_active_order(
        symbol=symbol,
        side=side,
        order_type="Market",
        qty=quantity,
        reduce_only=False,
        close_on_trigger=False,
        time_in_force="GoodTillCancel",
        take_profit=take_profit,
        stop_loss=stop_loss,
    )['result']


def get_active_orders(symbol):
    return session_auth.get_active_order(
        symbol=symbol
    )['result']


def get_order(order_id, symbol):
    return session_auth.get_active_order(
        order_id=order_id,
        symbol=symbol
    )['result']['data'][0]


def open_bybit_order(symbol, side, take_profit, stop_loss):
    quantity = get_order_quantity(symbol)
    order_placed = place_order(symbol, side, take_profit, stop_loss, quantity)
    return order_placed


def close_bybit_order(symbol, quantity):
    return session_auth.place_active_order(
        symbol=symbol,
        side="Sell",
        order_type="Market",
        qty=quantity,
        reduce_only=True,
        close_on_trigger=False,
        time_in_force="GoodTillCancel",
    )['result']


def get_bybit_interval(interval):
    match (interval):
        case '1m': return 1
        case '3m': return 3
        case '5m': return 5
        case '15m': return 15
        case '30m': return 30
        case '1h': return 60
        case '2h': return 120
        case '4h': return 240
        case '6h': return 360
        case '12h': return 720
        case '1d': return 'D'
        case '1w': return 'W'
        case '1M': return 'M'
        case _: return None


def auth(url):
    timestamp = int(time.time() * 10 ** 3)
    params = {
        "orderId": "1084090149712726016",
        "api_key": TEST_BYBIT_API_KEY,
        "timestamp": str(timestamp),
        "recv_window": "5000"
    }
    param_str = ''
    for key in sorted(params.keys()):
        v = params[key]
        if isinstance(params[key], bool):
            if params[key]:
                v = "true"
            else:
                v = "false"
        param_str += key + "=" + v + "&"
    param_str = param_str[:-1]
    signature = str(hmac.new(
        bytes(TEST_BYBIT_API_SECRET, "utf-8"),
        bytes(param_str, "utf-8"), digestmod="sha256"
    ).hexdigest())
    sign_real = {
        "sign": signature
    }
    param_str = quote_plus(param_str, safe="=&")
    full_param_str = f"{param_str}&sign={sign_real['sign']}"
    urllib3.disable_warnings()
    return f"{url}?{full_param_str}"
