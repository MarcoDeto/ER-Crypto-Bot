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


def get_delay(interval):
    match (interval):
        case '1m': return 10000
        case '3m': return 30000
        case '5m': return 50000
        case '15m': return 150000
        case '30m': return 300000
        case '1h': return 600000
        case '2h': return 1200000
        case '4h': return 2400000
        case '1d': return 14400000
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