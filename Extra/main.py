

import shutil
EMAS = [10, 20, 50]

def main(): 

    for newbot in EMAS:
        createBot(str(newbot))
            
def createBot(ema):
    try: 
        # MacBook path
        src = '/Users/marcodetomasi/WORK/bot/Er_Crypto_Bot'
        dst = '/Users/marcodetomasi/WORK/TESTs/XRP ' + ema
        # Windows path
        # src = '/WORK/bot/Er_Crypto_Bot'
        # dst = '/WORK/BOT/' + symbol
        file_path = dst + '/config.py'
        shutil.copytree(src, dst)
        f = open(file_path,"w")
        f.write("CONNECTION_STRING = 'mongodb+srv://dev:ManTyres@mantyres.fwdxdp6.mongodb.net'" + "\n")
        f.write("INTERVALS = ['1m', '3m', '5m', '15m', '30m', '1h', '2h', '4h', '1d']" + "\n")
        f.write("SECOND_EMAS = [25, 50, 60, 123, 200]" + "\n")
        f.write("MAIN_EMAS = [" + ema + "]" + "\n")
        f.write("BINANCE_API_KEY = 'ySBxTVFMkh3pGRyE1v8PqXXGbZoTcBs0eI2GuLvb99wjgWbQk3MiQxFjOH7SYqgC'" + "\n")
        f.write("BINANCE_API_SECRET = '6l2M7hMmg9AHprlFSMLER3xMSN735ioGgH69dY801aAKUvrNQs2KgP8JLLe9QSB7'" + "\n")
        f.write("SYMBOLS = ['" + 'XRP' + "']" + "\n")
        f.write("TEST_BINANCE_API_KEY = 'ffc4cfa52d1bce86cad01ab3f91b116ecda9d6ce2fbf4e3ff6e5bac28ec2c7c9'" + "\n")
        f.write("TEST_BINANCE_API_SECRET = '3c0b8577f414ddde728ab5dc3cb565b2c58d2be6060448e0adc0e4bbdfe88947'" + "\n")
        f.write("TELEGRAM_API_ID = 18943005" + "\n")
        f.write("TELEGRAM_API_HASH = '15b0d68a8f31361f902ddd4f11c30d1f'" + "\n")
        f.write("TELEGRAM_PHONE = '+39 3342927723'" + "\n")
        f.write("TELEGRAM_USERBNAME = 'blingus'" + "\n")
        f.write("TELEGRAM_CHANNEL = 'https://t.me/ercryptobotto'" + "\n")
        f.close()
    except Exception as f:
        print('main error: ', f)


if __name__ == '__main__':
    main()
