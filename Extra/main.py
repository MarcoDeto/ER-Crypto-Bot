

import shutil
from config import SYMBOLS


def main(): 

    for newbot in SYMBOLS:
        createBot(newbot)
            
def createBot(symbol):
    try:
        src = '/Users/marcodetomasi/WORK/bot/crypto_bot'
        dst = '/Users/marcodetomasi/WORK/TESTs/' + symbol
        file_path = dst + '/config.py'
        shutil.copytree(src, dst)
        f = open(file_path,"w")
        f.write("CONNECTION_STRING = 'mongodb+srv://dev:ManTyres@mantyres.fwdxdp6.mongodb.net'" + "\n")
        f.write("INTERVALS = ['1m', '3m', '5m', '15m', '30m', '45m', '1h', '2h', '3h', '4h', '1d']" + "\n")
        f.write("SECONDS_EMA = [25, 50, 60, 123]" + "\n")
        f.write("MAIN_EMA = 10" + "\n")
        f.write("api_key = 'ySBxTVFMkh3pGRyE1v8PqXXGbZoTcBs0eI2GuLvb99wjgWbQk3MiQxFjOH7SYqgC'" + "\n")
        f.write("api_secret = '6l2M7hMmg9AHprlFSMLER3xMSN735ioGgH69dY801aAKUvrNQs2KgP8JLLe9QSB7'" + "\n")
        f.write("SYMBOLS = ['" + symbol + "']" + "\n")
        f.write("START_DATE = '1 July, 2022'")
        f.close()
    except:
        pass


if __name__ == '__main__':
    main()