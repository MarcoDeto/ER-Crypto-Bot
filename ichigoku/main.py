from services.manager import *
from services.database.mongoDB import *
from services.messages.tradingview import *
from services.messages.telegram import *
from core import *

symbols = ['BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'BNBUSDT', 'XRPUSDT', 'DOTUSDT', 'MATICUSDT', 'AVAXUSDT']#, 'NEARUSDT', 'LINKUSDT', 'ATOMUSDT', 'XLMUSDT', 'XMRUSDT']

def __main__():
    
    global symbols
    #init_tradingview()
    #get_trading_view_graph('1m', 'BTCUSDT', 'BINANCE')
    init_telegram()
    my_channel = get_channel()
    timeDifference = get_time_difference()
    print("Making initial API call")
    print("Getting Kline Data")
    ichimokus = []
    symbols_data = []
    interval_i = 0
    for interval in INTERVALS:
        data = get_data(interval, symbols)
        symbols_data.append(data)
        dist_data = distribute_data(symbols_data[interval_i], interval)
        ichimokus.append(dist_data)
        interval_i = interval_i + 1
    print("Entering Loop")
    detect = get_detect(timeDifference)
    
    while True:
        interval_i = 0
        delay = int(get_time() - 10000 - timeDifference)
        for interval in INTERVALS:
            difference = int(delay // get_delay(interval))
            check_value = detect[interval_i]
            if(difference != check_value):
                detect[interval_i] = difference
                symbols_data[interval_i] = get_data(interval, symbols)
                ichimokus[interval_i] = distribute_data(symbols_data[interval_i], interval)
                print("renew " + interval)
                print(datetime.now())
            
            
            current_Prices = get_current_prices(symbols)
            price_i = 0
            for price in current_Prices:

                er_symbol = price.symbol
                er_price = price.price
                check_stop_loss(my_channel, er_symbol, interval, er_price)

                ichimokus_data = ichimokus[interval_i][price_i]
                kijun_sen = ichimokus_data[0].kijun_sen
                senkou_span_B = ichimokus_data[0].senkou_span_B
                check_trading_stops(my_channel, er_symbol, interval, er_price, kijun_sen)

                candles_data = symbols_data[interval_i][er_symbol]
                close_prices = get_close_prices(candles_data)
                check_take_profit(my_channel, er_symbol, interval, er_price, close_prices)

                larger_interval_trend = None
                if (interval_i != len(INTERVALS)-1):
                    larger_index = interval_i+1
                    larger_interval_trend = ichimokus[larger_index][price_i][2]
                
                if is_resp_tolerance(interval, er_price, senkou_span_B) == True:
                    coin = get_symbol(symbols[price_i])
                    check_break_out(coin, interval, close_prices, ichimokus_data, larger_interval_trend, my_channel)
                
                price_i = price_i + 1
     
            interval_i = interval_i + 1


__main__()