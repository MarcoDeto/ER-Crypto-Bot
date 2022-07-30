def get_max_candles(interval):
    match (interval):
        case '1m': return 4
        case '3m': return 6
        case '5m': return 7
        case '15m': return 12
        case '30m': return 17
        case '1h': return 2
        case '2h': return 2.5
        case '4h': return 6
        case '1d': return 18
        case _: return 1


def get_open_tollerance(interval):
    match (interval):
        case '1m': return 0.4
        case '3m': return 0.6
        case '5m': return 0.7
        case '15m': return 1.2
        case '30m': return 1.7
        case '1h': return 2
        case '2h': return 2.5
        case '4h': return 6
        case '1d': return 18
        case _: return 1


def get_stop_loss_tollerance(interval):
    match (interval):
        case '1m': return 1.5
        case '3m': return 2
        case '5m': return 2.5
        case '15m': return 4
        case '30m': return 7
        case '1h': return 9
        case '2h': return 12
        case '4h': return 15
        case '1d': return 15
        case _: return 1


def get_dt_db_tolerance(interval):
    match (interval):
        case '1m': return 0.05
        case '3m': return 0.10
        case '5m': return 0.15
        case '15m': return 0.3
        case '30m': return 0.5
        case '1h': return 0.7
        case '2h': return 1
        case '4h': return 1.2
        case '1d': return 1.7
        case _: return 0


def get_delay(interval):
    match (interval):
        case '1m': return 10000 # 10s
        case '3m': return 30000 # 30s
        case '5m': return 50000 # 50s
        case '15m': return 90000 # 1.5m
        case '30m': return 180000 # 3m
        case '1h': return 300000 # 5m
        case '2h': return 450000 # 7.5m
        case '4h': return 600000 # 10m
        case '1d': return 900000 # 15m
        case _: return 1


def get_timestap(interval):
    match (interval):
        case '1m': return 60 * 1000
        case '3m': return 60 * 3 * 1000
        case '5m': return 60 * 5 * 1000
        case '15m': return 60 * 15 * 1000
        case '30m': return 60 * 30 * 1000
        case '1h': return 60 * 60 * 1000
        case '2h': return 60 * 60 * 2 * 1000
        case '4h': return 60 * 60 * 4 * 1000
        case '1d': return 60 * 60 * 24 * 1000
        case _: return 1

def get_swing_tollerange(interval):
    match (interval):
        case '1m': return 1.5
        case '3m': return 3
        case '5m': return 3.5
        case '15m': return 6
        case '30m': return 7
        case '1h': return 8
        case '2h': return 14
        case '4h': return 25
        case '1d': return 35
        case '1w': return 40
        case _: return 1


'''
controllo le ultime 10 candele 
cerco l'indice del massimo e del minino

se min_index e max_index sono entrambi < 5
oppure se min_index e max_index sono entrambi >= 5
if candles[0] > candles[9]:
    return uptrend
else:
    return downtrend

if min_index >= 5:
    if candles[0] > min_price:
        return uptrend
    else:
        return downtrend
elif max_index >= 5:
    if candles[0] > max_price:
        return uptrend
    else:
        return downtrend
'''
 