from datetime import datetime
import numpy as np
from models.enums import CrossType, Status
from services.coins import checkOperation, createOperation, updateOperation
from services.mongoDB import getEMA, insertEMA, updateEMA
from config import MAIN_EMA, SECONDS_EMA 
import talib #pip3 install ta-lib


def checkEMAs(data, coin, interval):

    close_prices = get_close_data(data)

    for second_ema in SECONDS_EMA:

        ema_short = talib.EMA( close_prices, int(MAIN_EMA) )
        ema_long = talib.EMA( close_prices, int(second_ema) )

        try: 
            last_ema_short  = ema_short[-2]
            last_ema_long = ema_long[-2]
            ema_short = ema_short[-1]
            ema_long = ema_long[-1]
        except:
            continue

        if (ema_short > ema_long and last_ema_short < last_ema_long):
            Long(data[len(data)-1], coin, second_ema, interval)
        if (ema_short < ema_long and last_ema_short > last_ema_long):
            Short(data[len(data)-1], coin, second_ema, interval)


def getOperationDB(coin, second_ema, interval): 
    operationDB = getEMA(coin, second_ema, interval)
    if (operationDB):
        return operationDB
    return coin
    

def Long(candle, coin, second_ema, interval):

    print('LONG'+' '+interval+' '+str(second_ema)+' '+str(datetime.fromtimestamp(candle[0]/1000.0)))
    coin = getOperationDB(coin, second_ema, interval)
    newOperation = createOperation(coin, CrossType.LONG, second_ema, interval)
    emaCross = checkOperation(coin, CrossType.LONG, newOperation)
    if (emaCross == False): return

    if (emaCross.operation_type == Status.CLOSE):
        updateEMA(emaCross, coin, candle)
        emaCross = updateOperation(newOperation, coin, second_ema, interval)

    insertEMA(emaCross, candle)
        

def Short(candle, coin, second_ema, interval):
    
    print('SHORT'+' '+interval+' '+str(second_ema)+' '+str(datetime.fromtimestamp(candle[0]/1000.0)))
    coin = getOperationDB(coin, second_ema, interval)
    newOperation = createOperation(coin, CrossType.SHORT, second_ema, interval)
    emaCross = checkOperation(coin, CrossType.SHORT, newOperation)
    if (emaCross == False): return

    if (emaCross.operation_type == Status.CLOSE):
        updateEMA(emaCross, coin, candle)
        emaCross = updateOperation(newOperation, coin, second_ema, interval)

    insertEMA(emaCross, candle)


def get_close_data(data):
    return_data = []
    # prendendo i dati di chiusura per ogni kline
    for each in data:
        value = each[4]
        try: 
            # 4 è l'indice dei dati di chiusura in ogni kline
            value = float(each[4])
            return_data.append(value)
        except:
            pass

    # ritornando come array numpy per una migliore precisione e prestazioni
    return np.array(return_data)
