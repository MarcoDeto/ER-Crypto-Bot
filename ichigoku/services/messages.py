from services.discord import sendDiscordMessage
from services.telegram import sendTelegramMessage


def send_open_messages(my_channel, symbol, cross, open_price, link, time_frame):

    order = '**ORDER OPEN**\n\n'
    symbolCross = '**' + symbol + ' - BUY 🟢'
    openPrice = '\nOPEN PRICE**: ' + str(open_price) + ' 🛒'
    interval = '\n**TIME FRAME**: ' + str(time_frame)

    if (cross == 'SHORT'):
        symbolCross = '**' + symbol + ' - SELL 🔴'

    if (link != None):
        graph_link = '\n' + link + '\n'
    else:
        graph_link = ''

    message = order + symbolCross + openPrice + interval + graph_link
    sendTelegramMessage(my_channel, message)
    sendDiscordMessage(message)


def getMessage(symbol, cross, open_date, open_price, link, close_price, percent, seconds, time_frame, stop_loss=False):

    minutes = round(int(seconds) / 60, 1)
    order = '**ORDER CLOSE** ✅\n\n'
    symbolCross = '**' + symbol + ' - BUY 🟢'
    openDate = '\nOPEN DATE**:   ' + str(open_date) + ' 🗓'
    openPrice = '\n**OPEN PRICE**: ' + str(open_price) + ' 🛒'
    closePrice = '\n**CLOSE PRICE**: ' + str(close_price) + ' ✋🏼'
    profit = '\n**PROFIT**: ' + str(percent) + '% 🤑'
    duration = '\n**TIME**: ' + str(minutes) + 'm ⏰'
    interval = '\n**TIME FRAME**: ' + str(time_frame)

    if (cross == 'SHORT'):
        symbolCross = '**' + symbol + ' - SELL 🔴'
    if (percent < 0):
        order = '**ORDER CLOSE** ❌\n\n'
        profit = '\n**PROFIT**: ' + str(percent) + '% 😔'
    if (stop_loss == True):
        order = '**STOP LOSS** ❌\n\n'

    if (link != None):
        graph_link = '\n' + link + '\n'
    else:
        graph_link = ''

    return order + symbolCross + openDate + openPrice + closePrice + profit + duration + interval + graph_link


def send_close_messages(my_channel, link, symbol, cross, open_date, open_price, close_price, percent, seconds, time_frame, stop_loss=False):

    message = getMessage(symbol, cross, open_date, open_price, link, close_price, percent, seconds, time_frame, stop_loss)
 
    sendTelegramMessage(my_channel, message)
    sendDiscordMessage(message)
