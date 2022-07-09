from models.enums import CrossType, Status
from services.coins import checkOperation, createOperation, updateOperation
from services.mongoDB import getEMA, insertEMA, updateEMA
from config import MAIN_EMA, SECONDS_EMA 
import talib #pip3 install ta-lib


async def checkEMAs(data, coin, interval):

    for second_ema in SECONDS_EMA:

        ema_short = talib.EMA(data,int(MAIN_EMA))
        ema_long = talib.EMA(data,int(second_ema))
        last_ema_short  = ema_short[-2]
        last_ema_long = ema_long[-2]
        ema_short = ema_short[-1]
        ema_long = ema_long[-1]
        
        Long(coin, second_ema, interval)
        Short(coin, second_ema, interval)

        if (ema_short > ema_long and last_ema_short < last_ema_long):
            Long(coin, second_ema, interval)
        if (ema_short < ema_long and last_ema_short > last_ema_long):
            Short(coin, second_ema, interval)


def getOperationDB(coin, second_ema, interval): 
    operationDB = getEMA(coin, second_ema, interval)
    if (operationDB):
        return operationDB
    return coin
    

def Long(coin, second_ema, interval):
    print('LONG')
    coin = getOperationDB(coin, second_ema, interval)
    newOperation = createOperation(coin, CrossType.LONG, second_ema, interval)
    emaCross = checkOperation(coin, CrossType.LONG, newOperation)
    if (emaCross == False): return

    if (emaCross.operation_type == Status.CLOSE):
        updateEMA(emaCross, coin)
        emaCross = updateOperation(newOperation, coin, second_ema, interval)

    insertEMA(emaCross)
        

def Short(coin, second_ema, interval):
    print('SHORT')
    coin = getOperationDB(coin, second_ema, interval)
    newOperation = createOperation(coin, CrossType.SHORT, second_ema, interval)
    emaCross = checkOperation(coin, CrossType.SHORT, newOperation)
    if (emaCross == False): return

    if (emaCross.operation_type == Status.CLOSE):
        updateEMA(emaCross, coin)
        emaCross = updateOperation(newOperation, coin, second_ema, interval)

    insertEMA(emaCross)
