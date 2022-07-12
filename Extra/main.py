

import shutil
SYMBOLS = [
    #{#'base': 'BTC', 'date': '17 August, 2017'},
    {'base': 'ETH', 'date': '17 August, 2017'},
    {'base': 'BNB', 'date': '6 November, 2017'},
    {'base': 'XRP', 'date': '4 May, 2018'},
    {'base': 'ADA', 'date': '17 April, 2018'},
    {'base': 'LUNA', 'date': '21 August, 2020'},
    {'base': 'SOL', 'date': '11 August, 2020'},
    {'base': 'AVAX', 'date': '22 September, 2020'},
    {'base': 'DOT', 'date': '18 August, 2020'},
    {'base': 'DOGE', 'date': '5 July, 2019'},
    {'base': 'SHIB', 'date': '10 May, 2021'},
    {'base': 'CAKE', 'date': '19 February, 2021'},
    {'base': 'MATIC', 'date': '26 April, 2019'},
    {'base': 'DAI', 'date': '11 August, 2020'},
    {'base': 'LTC', 'date': '13 December, 2017'},
    {'base': 'ATOM', 'date': '29 April, 2019'},
    {'base': 'NEAR', 'date': '14 October, 2020'},
    {'base': 'LINK', 'date': '16 January, 2019'},
    {'base': 'UNI', 'date': '17 September, 2020'},
    {'base': 'BCH', 'date': '28 November, 2019'},
    {'base': 'ONE', 'date': '01 June, 2019'},
    {'base': 'TRX', 'date': '11 June, 2018'},
    {'base': 'ETC', 'date': '12 June, 2018'},
    {'base': 'CELO', 'date': '05 January, 2021'},
    {'base': 'ALGO', 'date': '22 June, 2019'},
    {'base': 'XLM', 'date': '31 May, 2018'},
    {'base': 'MANA', 'date': '06 August, 2020'},
    {'base': 'HBAR', 'date': '29 November, 2019'},
    {'base': 'APE', 'date': '17 March, 2022'},
    {'base': 'VET', 'date': '25 July, 2018'},
    {'base': 'GALA', 'date': '13 September, 2021'},
]

def main(): 

    for newbot in SYMBOLS:
        createBot(newbot)
            
def createBot(symbol):
    try: 
        # MacBook path
        src = '/Users/marcodetomasi/WORK/bot/Er_Crypto_Bot'
        dst = '/Users/marcodetomasi/WORK/TESTs/' + symbol['base']
        # Windows path
        # src = '/WORK/ER-Crypto-Bot/Er_Crypto_Bot'
        # dst = '/WORK/TESTs/' + symbol['base']
        file_path = dst + '/config.py'
        shutil.copytree(src, dst)
        f = open(file_path,"w")
        f.write("CONNECTION_STRING = 'mongodb+srv://dev:ManTyres@mantyres.fwdxdp6.mongodb.net'" + "\n")
        f.write("INTERVALS = ['5m', '15m', '30m', '45m', '1h', '2h', '3h', '4h', '1d']" + "\n")
        f.write("SECONDS_EMA = [25, 50, 60, 123]" + "\n")
        f.write("MAIN_EMA = 10" + "\n")
        f.write("api_key = 'ySBxTVFMkh3pGRyE1v8PqXXGbZoTcBs0eI2GuLvb99wjgWbQk3MiQxFjOH7SYqgC'" + "\n")
        f.write("api_secret = '6l2M7hMmg9AHprlFSMLER3xMSN735ioGgH69dY801aAKUvrNQs2KgP8JLLe9QSB7'" + "\n")
        f.write("SYMBOLS = ['" + symbol['base'] + "']" + "\n")
        f.write("START_DATE = '" + symbol['date'] + "'")
        f.close()
    except Exception as f:
        print('main error: ', f)


if __name__ == '__main__':
    main()
