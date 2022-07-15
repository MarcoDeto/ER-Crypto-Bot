from datetime import datetime
import numpy as np
from models.enums import CrossType, Status
from services.coins import checkOperation, createOperation, updateOperation
from services.conditions import getTimeframeOpenCheck
from config import MAIN_EMA, SECOND_EMAS 
import talib

from services.settings import getMaxDays, getMinDays #pip3 install ta-lib


async def checkCycle(start_price, data, coin, cycletype, my_channel):

    low_shadow_prices = await get_close_data(data)
    check = checkOpen(start_price, cycletype, data)
    # AGGIUNGERE IF CHECK != START PRIOCE

def checkOpen(start_price, cycletype, data):

    sub_cycle = getTimeframeOpenCheck(cycletype)
    maxdays = getMaxDays(sub_cycle)
    mindays = getMinDays(sub_cycle)
    start_index = np.where(data == start_price)
    start_range = start_index + mindays
    end_range = start_index + maxdays
    range = data[start_range:end_range]
    for candle in range:
        if (candle < start_price):
            return candle
        else:
            return start_price


def getOperationDB(coin, second_ema, interval): 
    operationDB = getEMA(coin, second_ema, interval)
    if (operationDB):
        return operationDB
    return coin
    

async def Long(coin, second_ema, interval):

    print('LONG'+' '+interval+' '+str(second_ema))
    coin = getOperationDB(coin, second_ema, interval)
    newOperation = createOperation(coin, CrossType.LONG, second_ema, interval)
    emaCross = checkOperation(coin, CrossType.LONG, newOperation)
    if (emaCross == False): return

    if (emaCross.operation_type == Status.CLOSE):
        await updateEMA(emaCross, coin)
        emaCross = updateOperation(newOperation, coin, second_ema, interval)

    await insertEMA(emaCross)
        

async def Short(coin, second_ema, interval):
    
    print('SHORT'+' '+interval+' '+str(second_ema))
    coin = getOperationDB(coin, second_ema, interval)
    newOperation = createOperation(coin, CrossType.SHORT, second_ema, interval)
    emaCross = checkOperation(coin, CrossType.SHORT, newOperation)
    if (emaCross == False): return

    if (emaCross.operation_type == Status.CLOSE):
        await updateEMA(emaCross, coin)
        emaCross = updateOperation(newOperation, coin, second_ema, interval)

    await insertEMA(emaCross)


async def get_close_data(data):
    return_data = []
    # prendendo i dati di chiusura per ogni kline
    for each in data:
        value = each[3]
        try: 
            # 4 è l'indice dei dati di chiusura in ogni kline
            value = float(each[3])
            return_data.append(value)
        except:
            pass

    # ritornando come array numpy per una migliore precisione e prestazioni
    return np.array(return_data)
