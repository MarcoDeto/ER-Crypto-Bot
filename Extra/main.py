

import shutil
SYMBOLS = ['BTC', 'ETH', 'SOL', 'BNB']

def main(): 

    for newbot in SYMBOLS:
        createBot(newbot)
            
def createBot(symbol):
    try: 
        # MacBook path
        src = '/Users/marcodetomasi/WORK/bot/Er_Crypto_Bot'
        dst = '/Users/marcodetomasi/WORK/TESTs/' + symbol
        # Windows path
        # src = '/WORK/bot/Er_Crypto_Bot'
        # dst = '/WORK/BOT/' + symbol
        file_path = dst + '/config.py'
        shutil.copytree(src, dst)
        f = open(file_path,"w")
        f.write("CONNECTION_STRING = 'mongodb+srv://dev:ManTyres@mantyres.fwdxdp6.mongodb.net'" + "\n")
        f.write("INTERVALS = ['1m', '3m', '5m', '15m', '30m', '1h', '2h', '4h', '1d']" + "\n")
        f.write("SECOND_EMAS = [25, 50, 60, 123, 200]" + "\n")
        f.write("MAIN_EMAS = [10, 20, 50]" + "\n")
        f.write("api_key = 'ySBxTVFMkh3pGRyE1v8PqXXGbZoTcBs0eI2GuLvb99wjgWbQk3MiQxFjOH7SYqgC'" + "\n")
        f.write("api_secret = '6l2M7hMmg9AHprlFSMLER3xMSN735ioGgH69dY801aAKUvrNQs2KgP8JLLe9QSB7'" + "\n")
        f.write("SYMBOLS = ['" + symbol + "']" + "\n")
        #f.write("START_DATE = '" + symbol['date'] + "'")
        f.close()
    except Exception as f:
        print('main error: ', f)


if __name__ == '__main__':
    main()
