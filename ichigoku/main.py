import math
from services.manager import *
from services.database.mongoDB import *
from services.messages.tradingview import *
from services.messages.telegram import *
from core import *


def __main__():
    
    #init_tradingview()
    #get_trading_view_graph('1m', 'BTCUSDT', 'BINANCE')
    init_telegram()
    telegram = get_channel()
    timeDifference = get_time_difference()
    print('Making initial API call')
    print('Getting Kline Data')
    ichimokus = []
    symbols_data = []
    interval_i = 0
    for interval in INTERVALS:
        data = get_data(interval, SYMBOLS)
        symbols_data.append(data)
        dist_data = distribute_data(symbols_data[interval_i], interval)
        ichimokus.append(dist_data)
        interval_i = interval_i + 1
    print('Entering Loop')
    detect = get_detect(timeDifference)
    
    while True:
        interval_i = 0
        delay = int(get_time() - 10000 - timeDifference)
        for interval in INTERVALS:
            difference = int(delay // get_delay(interval))
            check_value = detect[interval_i]
            if(difference != check_value):
                detect[interval_i] = difference
                symbols_data[interval_i] = get_data(interval, SYMBOLS)
                ichimokus[interval_i] = distribute_data(symbols_data[interval_i], interval)
                print('renew ' + interval)
                print(datetime.now())
            
            
            symbol_i = 0
            for symbol in SYMBOLS:
                
                price = get_price(symbol)
                check_stop_losses(telegram, symbol, price)

                ichimokus_data = ichimokus[interval_i][symbol_i]
                kijun_sen = ichimokus_data[0].kijun_sen
                senkou_span_B = ichimokus_data[0].senkou_span_B
                check_trailing_stops(telegram, symbol, interval, price, kijun_sen)

                candles_data = symbols_data[interval_i][symbol]
                close_prices = get_close_prices(candles_data)
                check_take_profits(telegram, symbol, interval, price, close_prices)
                
                if is_resp_tolerance(interval, price, senkou_span_B) == True:
                #TENERE CONTO DEL RETEST CON CIRCA DIECI CANDELE
                    
                    coin = get_symbol(SYMBOLS[symbol_i])
                    larger_interval_trend = None
                    if (interval_i != len(INTERVALS)-1):
                        larger_index = interval_i+1
                        larger_interval_trend = ichimokus[larger_index][symbol_i][2]
                    check_break_out(coin, interval, close_prices, ichimokus_data, larger_interval_trend, telegram)
                
                symbol_i = symbol_i + 1
     
            interval_i = interval_i + 1


__main__()