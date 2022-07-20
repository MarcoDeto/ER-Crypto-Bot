from tkinter import N
from services.utilities import *
from services.binance import *
from services.core import *
from models.ichimoku import *

symbols = ['BTCUSDT']

def __main__():
    global symbols    
    initTelegram()
    my_channel = getChannel()

    timeDifference = getTimeDifference()
    print("Making initial API call")
    print("Getting Kline Data")
    ichimokus = []
    symbols_data = []
    index = 0
    for interval in INTERVALS:
        data = getData(interval, symbols)
        symbols_data.append(data)
        dist_data = distribute_data(symbols_data[index], interval)
        ichimokus.append(dist_data)
        index = index + 1
    print("Entering Loop")
    detect = getDetect(timeDifference)
    while True:
        index = 0
        delay = int(getTime() - 10000 - timeDifference)
        for interval in INTERVALS:
            difference = int(delay // getDelay(interval))
            check_value = detect[index]
            if(difference != check_value):
                detect[index] = difference
                symbols_data[index] = getData(interval, symbols)
                ichimokus[index] = distribute_data(symbols_data[index], interval)
                print("renew " + interval)
                print(datetime.now())
            
            
            current_Prices = getCurrentPrices(symbols)
            price_index = 0
            for price in current_Prices:

                checkStopLoss(price.symbol, price.price, my_channel)

                ichimokus_data = ichimokus[index][price_index]
                kijun_sen = ichimokus_data[0].kijun_sen
                checkTakeProfit(price.symbol, interval, price.price, kijun_sen, my_channel)

                candles_data = symbols_data[index][price.symbol]
                checkBreakOut(interval, candles_data, ichimokus_data, price, my_channel)
                price_index = price_index + 1
     
            index = index + 1


def distribute_data(datadict, interval):
    result = []
    for symbol in datadict:
        ichimokuStatus = setInitialData(datadict[symbol], interval)
        result.append(ichimokuStatus)
    return result

__main__()