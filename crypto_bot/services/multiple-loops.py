import asyncio
import json
import websocket

async def do_something(delay, message):
   while True:
      await asyncio.sleep(delay)
      print(message)

def main():
    loop = asyncio.get_event_loop()
    loop.create_task(do_something(1, "delay equals 1"))
    loop.create_task(do_something(3, "delay equals 3"))
    loop.run_forever()
if __name__ == '__main__':
    try:
        main()
    except Exception as f:
        print('main error: ', f)


# websocket.enableTrace(True) #uncomment for debug

def on_open(ws):
    print("open")

def on_message(ws,message):
    json_message = json.loads(message)
    candle = json_message['data']['k']
    print(message)
    is_candle_closed = candle['x']
    if is_candle_closed:
        print(json.dumps(candle, indent=2))

def on_close(ws, close_status_code, close_msg):
    print("closed")

def newtest():
    cc = 'btcusdt'
    interval = '1m'
    socket = f'wss://stream.binance.com:9443/ws/{cc}t@kline_{interval}'
    SOCK = "wss://stream.binance.com:9443/stream?streams=ethusdt@kline_1m/btcusdt@kline_1m/bnbusdt@kline_1m/ethbtc@kline_1m"
    ws = websocket.WebSocketApp(SOCK, on_open=on_open,on_close=on_close, on_message=on_message)
    ws.run_forever()