from services.messages.discord import sendDiscordMessage
from services.messages.telegram import sendTelegramMessage


def send_open_messages(my_channel, link, operation):

    order = '**ORDER OPEN**\n\n'
    symbolCross = '**' + operation['symbol'] + ' - BUY 🟢'
    openPrice = '\nOPEN PRICE**: ' + str(operation['open_price']) + ' 🛒'
    interval = '\n**TIME FRAME**: ' + str(operation['time_frame'])

    if (operation['cross'] == 'SHORT'):
        symbolCross = '**' + operation['symbol'] + ' - SELL 🔴'

    if (link != None):
        graph_link = '\n' + link + '\n'
    else:
        graph_link = ''

    message = order + symbolCross + openPrice + interval + graph_link
    sendTelegramMessage(my_channel, message)
    sendDiscordMessage(message)


def send_close_messages(my_channel, link, operation, stop_loss=False):
    order = ''
    profit = ''
    graph_link = ''
    minutes = round(int(operation['seconds']) / 60, 1)
    symbolCross = '**' + operation['symbol'] + ' - BUY 🟢'
    if (operation['cross'] == 'SHORT'):
        symbolCross = '**' + operation['symbol'] + ' - SELL 🔴'
    openDate = '\nOPEN DATE**:   ' + str(operation['open_date']) + ' 🗓'
    openPrice = '\n**OPEN PRICE**: ' + str(operation['open_price']) + ' 🛒'
    closePrice = '\n**CLOSE PRICE**: ' + str(operation['close_price']) + ' ✋🏼'
    duration = '\n**TIME**: ' + str(minutes) + 'm ⏰'
    interval = '\n**TIME FRAME**: ' + str(operation['time_frame'])

    if (stop_loss == True):
        order = '**STOP LOSS** ❌\n\n'
    else:
        if (operation['percent'] < 0):
            order = '**ORDER CLOSE** ❌\n\n'
            profit = '\n**PROFIT**: ' + str(operation['percent']) + '% 😔'
        else:
            order = '**ORDER CLOSE** ✅\n\n'
            profit = '\n**PROFIT**: ' + str(operation['percent']) + '% 🤑'

    if (link != None):
        graph_link = '\n' + link + '\n'
    else:
        graph_link = ''

    message = order + symbolCross + openDate + openPrice + closePrice + profit + duration + interval + graph_link
 
    sendTelegramMessage(my_channel, message)
    sendDiscordMessage(message)
