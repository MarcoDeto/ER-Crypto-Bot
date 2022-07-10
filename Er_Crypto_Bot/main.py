from datetime import date, datetime, timedelta
from config import START_DATE
from services.mongoDB import dropCollection
from config import INTERVALS
from services.binance import getSymbols, get_historical_klines
from services.coins import isToSkip
from services.emas import checkEMAs


def main():
    # cancello tutti i dati sul DB
    # dropCollection()
    print('\nSTART')
    print(datetime.now())
    Symbols = getSymbols()
    coin = Symbols[0]
    symbol = coin['symbol']
    if (isToSkip(symbol)):
        return
    startDate = datetime.strptime(START_DATE, "%d %B, %Y")
    endDate = startDate + timedelta(days=2)
    data = get_historical_klines(symbol, INTERVALS[0], startDate, endDate)
    for interval in INTERVALS:
        endDate = startDate + timedelta(days=getDays(interval))
        data = get_historical_klines(symbol, interval, startDate, endDate)
        klines = len(data)
        if (klines < 300):
            print('There are less than 300 candles! Not accurate calculation!')
            return
        candles = data[0:299]
        lastLoop = False
        while True:
            if (lastLoop == True):
                return
            checkEMAs(candles, coin, interval)
            candles.append(data[len(candles)])
            if (len(candles) == klines):
                data = data[(klines-300):]
                candles = candles[(klines-300):]
                startDate = startDate + timedelta(days=getDays(interval))
                endDate = endDate + timedelta(days=getDays(interval))
                toAppend = get_historical_klines(
                    symbol, interval, startDate, endDate)
                for candle in toAppend:
                    data.append(candle)
            if (endDate.date() >= date.today() and len(candles) == klines):
                lastLoop = True


def getDays(interval):
    match interval:
        case '5m':
            return 2
        case '15m':
            return 4
        case '30m':
            return 8
        case '45m':
            return 16
        case '1h':
            return 24
        case '2h':
            return 48
        case '3h':
            return 72
        case '4h':
            return 96
        case '1d':
            return 350
        case _:
            return 1


if __name__ == '__main__':
    main()
    # try:
    #     main()
    # except Exception as f:
    #     print('main error: ', f)
