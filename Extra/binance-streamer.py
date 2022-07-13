import json
import websocket
import datetime

from config import INTERVALS


def on_message(ws, message):
    print('\n')
    print(str(datetime.datetime.now()) + ": ")
    result = json.loads(message)
    print(result['k']['i'])
    print(message)


def on_error(ws, error):
    print(error)


def on_close(close_msg):
    print("### closed ###" + close_msg)


def streamKline(currency, interval):

    websocket.enableTrace(False)
    socket = f'wss://stream.binance.com:9443/ws/{currency}@kline_{interval}'
    socket2 = f'wss://stream.binance.com:9443/ws/{currency}@kline_5m'
    ws = websocket.WebSocketApp(
        socket, on_message=on_message, on_error=on_error, on_close=on_close)
    ws2 = websocket.WebSocketApp(
        socket2, on_message=on_message, on_error=on_error, on_close=on_close)
    ws.run_forever()
    ws2.run_forever()


def intervalsLopp():
    for interval in INTERVALS:
        streamKline('solusdt', interval)


intervalsLopp()
