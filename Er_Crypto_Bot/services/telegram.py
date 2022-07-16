# from telegram import Bot
# import telepot

# from config import TELEGRAM_TOKEN

# def TelegramSend():
#    token = '1975899152:AAHvtQtu0ry-S8oOF17-AxC4giE6u-kctJs' # telegram token
#    receiver_id = "https://t.me/ercryptobotto" # https://api.telegram.org/bot<TOKEN>/getUpdates

#    bot = Bot(TELEGRAM_TOKEN)
#    bot.send_message(receiver_id, "cccccccc")
#    bot = telepot.Bot(TELEGRAM_TOKEN)

#    bot.sendMessage(receiver_id, 'This is a automated test message.') # send a activation message to telegram receiver id

#    bot.sendPhoto(receiver_id, photo=open('test_img.png', 'rb')) # send message to telegram

import time
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError

from config import TELEGRAM_API_HASH, TELEGRAM_API_ID, TELEGRAM_CHANNEL, TELEGRAM_PHONE, TELEGRAM_USERBNAME

client = TelegramClient(TELEGRAM_USERBNAME, TELEGRAM_API_ID, TELEGRAM_API_HASH)

async def initTelegram():

    await client.start()
    print("Telegram Client Created")
    # Ensure you're authorized
    if await client.is_user_authorized() == False:
        await client.send_code_request(TELEGRAM_PHONE)
        try:
            await client.sign_in(TELEGRAM_PHONE, input('Enter the code: '))
        except SessionPasswordNeededError:
            await client.sign_in(password=input('Password: '))

async def getChannel():
    return await client.get_entity(TELEGRAM_CHANNEL)
    

async def sendMessage(my_channel, symbol, cross, open_date, open_price, close_price, percent, seconds, stop_loss = False):
    
    minutes = round(seconds / 60, 1)
    order = '**ORDER CLOSE** ✅\n\n'
    symbolCross = '**' + symbol + ' - BUY 🟢'
    openDate = '\nOPEN DATE**:   ' + str(open_date) + ' 🗓'
    openPrice = '\n**OPEN PRICE**: ' + str(open_price) + ' 🛒'
    closePrice = '\n**CLOSE PRICE**: ' + str(close_price) + ' ✋🏼'
    profit = '\n**PROFIT**: ' + str(percent) + '% 🤑'
    duration = '\n**TIME**: ' + str(minutes) + 'm ⏰'

    if (cross == 'SHORT'):
        symbolCross = '**' + symbol + '**' + ' - SELL 🔴**'
    if (percent < 0):
        order = '**ORDER CLOSE** ❌\n\n'
    if (stop_loss == True):
        order = '**STOP LOSS** ❌\n\n'

    message = order + symbolCross + openDate + openPrice + closePrice + profit + duration

    await client.send_message(my_channel, message)


