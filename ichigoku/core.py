from services.coins import *
from services.mongoDB import *
from models.enums import *
from services.utilities import *


def checkBreakOut(interval, symbols_data, ichimokus_data, price, my_channel):
    current = ichimokus_data[0]
    last = ichimokus_data[1]
    last_senkou_span_B = last.senkou_span_B
    last_price = last.close_price
    senkou_span_B = current.senkou_span_B
    # close_price = current.close_price
    current_price = float(price.price)
    coin = getSymbol(price.symbol)

    #strategia doppio massimo o doppio minimo sul trand e -26 candele su rsi
    #close_prices = get_close_prices(symbols_data)
    #double_max_rsi(close_prices)


    if (current_price > senkou_span_B and last_price < last_senkou_span_B):

        if_long_open(coin, interval, my_channel)

        close_prices = get_close_prices(symbols_data)
        if (RSIIsAlert(close_prices) == RSIType.OVERBOUGHT):
            openLong(coin, interval, my_channel)

    if (current_price < senkou_span_B and last_price > last_senkou_span_B):

        if_short_open(coin, interval, my_channel)

        close_prices = get_close_prices(symbols_data)
        if (RSIIsAlert(close_prices) == RSIType.OVERSOLD):
            openShort(coin, interval, my_channel)


def openLong(coin, interval, my_channel):
    print('LONG'+' '+interval)
    newOperation = createOperation(coin, CrossType.LONG, interval)
    # coin = getOperationDB(coin, interval)
    span_B_cross = checkOperation(coin, CrossType.LONG, newOperation)
    if (span_B_cross == False):
        return

    # if (span_B_cross.operation_type == Status.CLOSE):
    #     updateIchiGoku(span_B_cross, coin, my_channel)
    #     span_B_cross = updateOperation(newOperation, coin, interval)

    insertIchiGoku(span_B_cross, my_channel)


def openShort(coin, interval, my_channel):
    print('SHORT'+' '+interval)
    newOperation = createOperation(coin, CrossType.SHORT, interval)
    # coin = getOperationDB(coin, interval)
    span_B_cross = checkOperation(coin, CrossType.SHORT, newOperation)
    if (span_B_cross == False):
        return

    #if (span_B_cross.operation_type == Status.CLOSE):
    #    updateIchiGoku(span_B_cross, coin, my_channel)
    #    span_B_cross = updateOperation(newOperation, coin, interval)

    insertIchiGoku(span_B_cross, my_channel)


def if_long_open(coin, interval, my_channel):
    open_operation = checkIfOpen(coin ,'LONG', interval)
    if (open_operation != None):
        insertIchiGoku(coin, my_channel)


def if_short_open(coin, interval, my_channel):
    open_operation = checkIfOpen(coin, 'SHORT', interval)
    if (open_operation != None):
        insertIchiGoku(coin, my_channel)
