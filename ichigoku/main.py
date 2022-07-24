from services.manager import *
from services.database.mongoDB import *
from services.messages.tradingview import *
from services.messages.telegram import *
from core import *

symbols = ['BTCUSDT']

def __main__():
    
    global symbols
    #init_tradingview()
    #get_trading_view_graph('1m', 'BTCUSDT', 'BINANCE')
    init_telegram()
    my_channel = get_channel()
    timeDifference = getTimeDifference()
    print("Making initial API call")
    print("Getting Kline Data")
    ichimokus = []
    symbols_data = []
    interval_i = 0
    for interval in INTERVALS:
        data = getData(interval, symbols)
        symbols_data.append(data)
        dist_data = distribute_data(symbols_data[interval_i], interval)
        ichimokus.append(dist_data)
        interval_i = interval_i + 1
    print("Entering Loop")
    detect = get_detect(timeDifference)
    coin = getSymbol(symbols[0])
    while True:
        interval_i = 0
        delay = int(get_time() - 10000 - timeDifference)
        for interval in INTERVALS:
            difference = int(delay // get_delay(interval))
            check_value = detect[interval_i]
            if(difference != check_value):
                detect[interval_i] = difference
                symbols_data[interval_i] = getData(interval, symbols)
                ichimokus[interval_i] = distribute_data(symbols_data[interval_i], interval)
                print("renew " + interval)
                print(datetime.now())
            
            
            current_Prices = getCurrentPrices(symbols)
            price_i = 0
            for price in current_Prices:

                check_stop_loss(my_channel, price.symbol, price.price)

                ichimokus_data = ichimokus[interval_i][price_i]
                kijun_sen = ichimokus_data[0].kijun_sen

                check_trading_stops(my_channel, price.symbol, interval, price.price, kijun_sen)

                candles_data = symbols_data[interval_i][price.symbol]
                close_prices = get_close_prices(candles_data)

                check_take_profit(my_channel, price.symbol, interval, price.price, close_prices)

                larger_interval_trend = None
                if (interval_i != len(INTERVALS)-1):
                    larger_index = interval_i+1
                    larger_interval_trend = ichimokus[larger_index][price_i][2]
                
                checkBreakOut(coin, interval, close_prices, ichimokus_data, larger_interval_trend, my_channel)
                price_i = price_i + 1
     
            interval_i = interval_i + 1


__main__()