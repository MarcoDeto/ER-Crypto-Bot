from datetime import datetime
import numpy as np
from models.enums import CrossType, Status
from services.coins import checkOperation, createOperation, updateOperation
from services.mongoDB import getEMA, insertEMA, checkStopLoss, updateEMA
from config import MAIN_EMAS, SECOND_EMAS 
import talib #pip3 install ta-lib


async def checkEMAs(data, coin, interval):

    close_prices = await get_close_data(data)

    priceToCheck = close_prices[len(close_prices) - 1]
    await checkStopLoss(coin['symbol'], priceToCheck)

    for main_ema in MAIN_EMAS:
        for second_ema in SECOND_EMAS:

            ema_short = talib.EMA( close_prices, int(main_ema) )
            ema_long = talib.EMA( close_prices, int(second_ema) )

            try: 
                last_ema_short  = ema_short[-2]
                last_ema_long = ema_long[-2]
                ema_short = ema_short[-1]
                ema_long = ema_long[-1]
            except:
                continue

            if (ema_short > ema_long and last_ema_short < last_ema_long):
                await Long(coin, main_ema, second_ema, interval)
            if (ema_short < ema_long and last_ema_short > last_ema_long):
                await Short(coin, main_ema, second_ema, interval)


def getOperationDB(coin, main_ema, second_ema, interval): 
    operationDB = getEMA(coin, main_ema, second_ema, interval)
    if (operationDB):
        return operationDB
    return coin
    

async def Long(coin, main_ema, second_ema, interval):

    print('LONG'+' '+interval+' '+str(second_ema))
    coin = getOperationDB(coin, main_ema, second_ema, interval)
    newOperation = createOperation(coin, CrossType.LONG, main_ema, second_ema, interval)
    emaCross = checkOperation(coin, CrossType.LONG, newOperation)
    if (emaCross == False): return

    if (emaCross.operation_type == Status.CLOSE):
        await updateEMA(emaCross, coin)
        emaCross = updateOperation(newOperation, coin, main_ema, second_ema, interval)

    await insertEMA(emaCross)
        

async def Short(coin, main_ema, second_ema, interval):
    
    print('SHORT'+' '+interval+' '+str(second_ema))
    coin = getOperationDB(coin, main_ema, second_ema, interval)
    newOperation = createOperation(coin, CrossType.SHORT, main_ema, second_ema, interval)
    emaCross = checkOperation(coin, CrossType.SHORT, newOperation)
    if (emaCross == False): return

    if (emaCross.operation_type == Status.CLOSE):
        await updateEMA(emaCross, coin)
        emaCross = updateOperation(newOperation, coin, main_ema, second_ema, interval)

    await insertEMA(emaCross)


async def get_close_data(data):
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
