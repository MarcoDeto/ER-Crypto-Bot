from services.messages.discord import sendDiscordMessage
from services.messages.telegram import sendTelegramMessage


def send_open_messages(telegram, link, operation):

    order = ' \n🎉 🆕 🥳' + '\n**ORDER OPEN**\n\n'
    symbol_cross = '**' + operation['symbol'] + ' - BUY 🟢'
    interval = '\n**TIME FRAME**: ' + str(operation['time_frame']) + ' 🕒'
    open_price = '\nOPEN PRICE**: ' + str(operation['open_price']) + ' 🛒'
    stop_loss = '\n**STOP LOSS**: ' + str(operation['stop_loss']) + ' ⏹'
    take_profit = '\n**TAKE PROFIT**: ' + str(operation['take_profit']) + ' 💸'

    if (operation['cross'] == 'SHORT'):
        symbol_cross = '**' + operation['symbol'] + ' - SELL 🔴'

    graph_link = '' if link == None else str('\n' + link + '\n')

    message = order + symbol_cross + open_price + stop_loss + take_profit + interval + graph_link
    sendTelegramMessage(telegram, message)
    sendDiscordMessage(message)


def send_close_messages(telegram, link, operation, status):
    start = ''
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

    percent = operation['percent']
    if (percent < 0):
        start = '\n \n❌❌❌\n'
        order = '**'+status+'** ❌\n\n'
        profit = '\n**PROFIT**: ' + str(percent) + '% 😔'
    else:
        start = '\n \n✅✅✅\n'
        order = '**'+status+'** ✅\n\n'
        profit = '\n**PROFIT**: ' + str(percent) + '% 🤑'

    graph_link = '' if link == None else str('\n' + link + '\n')

    message = start + order + symbolCross + openDate + openPrice + closePrice + profit + duration + interval + graph_link
 
    sendTelegramMessage(telegram, message)
    sendDiscordMessage(message)
