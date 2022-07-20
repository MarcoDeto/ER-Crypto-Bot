from services.coins import *
from services.mongoDB import *
from models.enums import *
from services.utilities import *


def checkBreakOut(interval, symbols_data, ichimokus_data, price, my_channel):
    current = ichimokus_data[0]
    last = ichimokus_data[1]
    last_senkou_span_B  = last.senkou_span_B
    last_price = last.close_price
    senkou_span_B = current.senkou_span_B
    # close_price = current.close_price
    current_price = float(price.price)

    if (current_price > senkou_span_B and last_price < last_senkou_span_B):
        close_prices = get_close_prices(symbols_data)
        if (RSIIsAlert(close_prices) == RSIType.OVERBOUGHT):
            coin = getSymbol(price.symbol)
            openLong(coin, interval, my_channel)

    if (current_price < senkou_span_B and last_price > last_senkou_span_B):
        close_prices = get_close_prices(symbols_data)
        if (RSIIsAlert(close_prices) == RSIType.OVERSOLD):
            coin = getSymbol(price.symbol)
            openShort(coin, interval, my_channel)


def openLong(coin, interval, my_channel):
    print('LONG'+' '+interval)
    # coin = getOperationDB(coin, interval)
    newOperation = createOperation(coin, CrossType.LONG, interval)
    emaCross = checkOperation(coin, CrossType.LONG, newOperation)

    if (emaCross == False): return

    if (emaCross.operation_type == Status.CLOSE):
        updateIchiGoku(emaCross, coin, my_channel)
        emaCross = updateOperation(newOperation, coin, interval)

    insertIchiGoku(emaCross)


def openShort(coin, interval, my_channel):
    
    print('SHORT'+' '+interval)
    # coin = getOperationDB(coin, interval)
    newOperation = createOperation(coin, CrossType.SHORT, interval)
    emaCross = checkOperation(coin, CrossType.SHORT, newOperation)
    if (emaCross == False): return

    if (emaCross.operation_type == Status.CLOSE):
        updateIchiGoku(emaCross, coin, my_channel)
        emaCross = updateOperation(newOperation, coin, interval)

    insertIchiGoku(emaCross)

