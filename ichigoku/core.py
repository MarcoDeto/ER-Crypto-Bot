from services.manager import *
from services.coins import *
from services.database.mongoDB import *
from models.enums import *
from services.utilities import *


def check_break_out(coin, interval, close_prices, ichimokus_data, larger_interval_trend, my_channel):
    current = ichimokus_data[0]
    last = ichimokus_data[1]
    last_senkou_span_B = last.senkou_span_B
    last_price = last.close_price
    senkou_span_B = current.senkou_span_B
    close_price = current.close_price
    
    #LONG
    if (close_price > senkou_span_B and last_price < last_senkou_span_B):

        if larger_interval_trend == Trend.DOWNTREND:
            return

        is_added = is_just_added(coin, 'LONG', interval)
        if is_added == True: return 

        elif is_added == False: 
            openLong(coin, interval, my_channel)
        
        elif is_added == None:
            if (RSIIsAlert(close_prices) == RSIType.OVERBOUGHT):
                openLong(coin, interval, my_channel)

    #SHORT
    if (close_price < senkou_span_B and last_price > last_senkou_span_B):

        if (larger_interval_trend == Trend.UPTREND):
            return

        is_added = is_just_added(coin, 'SHORT', interval)
        if is_added == True: return 

        elif is_added == False: 
            openShort(coin, interval, my_channel)

        elif is_added == None:
            if (RSIIsAlert(close_prices) == RSIType.OVERSOLD):
                openShort(coin, interval, my_channel)


def openLong(coin, interval, my_channel):
    print('LONG'+' '+interval)
    newOperation = createOperation(coin, CrossType.LONG, interval)
    coin = getOperationDB(coin, CrossType.LONG, interval)
    span_B_cross = checkOperation(coin, CrossType.LONG, newOperation)
    if (span_B_cross == False):
        return

    open_operation(my_channel, span_B_cross)


def openShort(coin, interval, my_channel):
    print('SHORT'+' '+interval)
    newOperation = createOperation(coin, CrossType.SHORT, interval)
    coin = getOperationDB(coin, CrossType.SHORT, interval)
    span_B_cross = checkOperation(coin, CrossType.SHORT, newOperation)
    if (span_B_cross == False):
        return

    open_operation(my_channel, span_B_cross)


def is_just_added(coin, cross, interval):
    open_operation = checkIfOpen(coin, cross, interval)

    if (open_operation == None): return None

    open_timestap = datetime.timestamp(open_operation['open_date'])
    now = datetime.now()
    now_timestap = datetime.timestamp(now)
    diff = now_timestap - open_timestap
    if (diff < get_timestap(interval)):
        return True
    return False


