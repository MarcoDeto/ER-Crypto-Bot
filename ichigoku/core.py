from services.manager import *
from services.coins import *
from services.database.mongoDB import *
from models.enums import *
from services.utilities import *


def check_break_out(coin, interval, close_prices, ichimokus_data, larger_interval_trend, telegram):
    current = ichimokus_data[0]
    last = ichimokus_data[1]
    last_senkou_span_B = last.senkou_span_B
    last_price = last.close_price
    senkou_span_B = current.senkou_span_B
    close_price = current.close_price

    # CAMBIARE LOGICA RICONOSCIMENTO TRAND INDICATORE DMI
    # RITEST SE SI AVVICINA A SPAN B DI UNA CERTA PERCENTUALE
    # AGGIUNGERE CONTROLLO POSIZIONE MEDIE PRIMA DI APRIRE
    # AGGIUNGERE AMPIEZZA ICHIMOKU
    
    #LONG
    if (close_price > senkou_span_B and last_price < last_senkou_span_B):

        if larger_interval_trend == Trend.DOWNTREND:
            return

        is_added = is_just_added(coin, 'LONG', interval)
        if is_added == True: return 

        elif is_added == False: 
            open_long(coin, interval, telegram)
        
        elif is_added == None:
            if (RSI_is_alert(close_prices) == RSIType.OVERBOUGHT):
                open_long(coin, interval, telegram)

    #SHORT
    if (close_price < senkou_span_B and last_price > last_senkou_span_B):

        if (larger_interval_trend == Trend.UPTREND):
            return

        is_added = is_just_added(coin, 'SHORT', interval)
        if is_added == True: return 

        elif is_added == False: 
            open_short(coin, interval, telegram)

        elif is_added == None:
            if (RSI_is_alert(close_prices) == RSIType.OVERSOLD):
                open_short(coin, interval, telegram)


def open_long(coin, interval, telegram):
    print('LONG'+' '+interval)
    newOperation = create_operation(coin, CrossType.LONG, interval)
    coin = get_operation_DB(coin, CrossType.LONG, interval)
    span_B_cross = check_operation(coin, CrossType.LONG, newOperation)
    if (span_B_cross == False):
        return

    open_operation(telegram, span_B_cross)


def open_short(coin, interval, telegram):
    print('SHORT'+' '+interval)
    newOperation = create_operation(coin, CrossType.SHORT, interval)
    coin = get_operation_DB(coin, CrossType.SHORT, interval)
    span_B_cross = check_operation(coin, CrossType.SHORT, newOperation)
    if (span_B_cross == False):
        return

    open_operation(telegram, span_B_cross)


def is_just_added(coin, cross, interval):
    open_operation = check_if_open(coin, cross, interval)
    if (open_operation == None): return None

    open_timestap = datetime.timestamp(open_operation['open_date'])
    now = datetime.now()
    now_timestap = datetime.timestamp(now)
    diff = now_timestap - open_timestap
    if (diff < get_timestap(interval)):
        return True
    return False


