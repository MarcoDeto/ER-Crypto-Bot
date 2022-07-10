

import shutil
SYMBOLS = [
    {'BTC', '17 August, 2017'},
    {'ETH', '17 August, 2017'},
    {'BNB', '6 November, 2017'},
    {'XRP', '4 May, 2018'},
    {'ADA', '17 April, 2018'},
    {'LUNA', '21 August, 2020'},
    {'SOL', '11 August, 2020'},
    {'AVAX', '22 September, 2020'},
    {'DOT', '18 August, 2020'},
    {'DOGE', '5 July, 2019'},
    {'SHIB', '10 May, 2021'},
    {'CAKE', '19 February, 2021'},
    {'MATIC', '26 April, 2019'},
    {'DAI', '11 August, 2020'},
    {'LTC', '13 December, 2017'},
    {'ATOM', '29 April, 2019'},
    {'NEAR', '14 October, 2020'},
    {'LINK', '16 January, 2019'},
    {'UNI', '17 September, 2020'},
    {'BCH', '28 November, 2019'},
    {'ONE', '01 June, 2019'},
    {'TRX', '11 June, 2018'},
    {'ETC', '12 June, 2018'},
    {'CELO', '05 January, 2021'},
    {'ALGO', '22 June, 2019'},
    {'XLM', '31 May, 2018'},
    {'MANA', '06 August, 2020'},
    {'HBAR', '29 November, 2019'},
    {'APE', '17 March, 2022'},
    {'VET', '25 July, 2018'},
    {'GALA', '13 September, 2021'},
]

def main(): 

    for newbot in SYMBOLS:
        createBot(newbot)
            
def createBot(symbol):
    try: 
        # src = '/Users/marcodetomasi/WORK/bot/crypto_bot'
        # dst = '/Users/marcodetomasi/WORK/TESTs/' + symbol
        src = '/WORK/ER-Crypto-Bot/Er_Crypto_Bot'
        dst = '/WORK/TESTs/' + symbol[0]
        file_path = dst + '/config.py'
        shutil.copytree(src, dst)
        f = open(file_path,"w")
        f.write("CONNECTION_STRING = 'mongodb+srv://dev:ManTyres@mantyres.fwdxdp6.mongodb.net'" + "\n")
        f.write("INTERVALS = ['5m', '15m', '30m', '45m', '1h', '2h', '3h', '4h', '1d']" + "\n")
        f.write("SECONDS_EMA = [25, 50, 60, 123]" + "\n")
        f.write("MAIN_EMA = 10" + "\n")
        f.write("api_key = 'ySBxTVFMkh3pGRyE1v8PqXXGbZoTcBs0eI2GuLvb99wjgWbQk3MiQxFjOH7SYqgC'" + "\n")
        f.write("api_secret = '6l2M7hMmg9AHprlFSMLER3xMSN735ioGgH69dY801aAKUvrNQs2KgP8JLLe9QSB7'" + "\n")
        f.write("SYMBOLS = ['" + symbol[0] + "']" + "\n")
        f.write("START_DATE = '" + symbol[1] + "'")
        f.close()
    except Exception as f:
        print('main error: ', f)


if __name__ == '__main__':
    main()