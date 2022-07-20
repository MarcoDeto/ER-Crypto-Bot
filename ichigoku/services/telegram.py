from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError

from config import TELEGRAM_API_HASH, TELEGRAM_API_ID, TELEGRAM_CHANNEL, TELEGRAM_PHONE, TELEGRAM_USERBNAME

client = TelegramClient(TELEGRAM_USERBNAME, TELEGRAM_API_ID, TELEGRAM_API_HASH)

def initTelegram():
    with client:
        client.loop.run_until_complete(getAccess())


async def getAccess():
    await client.start()
    print("Telegram Client Created")
    # Ensure you're authorized
    if await client.is_user_authorized() == False:
        await client.send_code_request(TELEGRAM_PHONE)
        try:
            await client.sign_in(TELEGRAM_PHONE, input('Enter the code: '))
        except SessionPasswordNeededError:
            await client.sign_in(password=input('Password: '))


def getChannel():
    with client:
        return client.loop.run_until_complete(client.get_entity(TELEGRAM_CHANNEL))
    

def sendMessage(my_channel, symbol, cross, open_date, open_price, close_price, percent, seconds, time_frame, stop_loss = False):
    
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

    message = order + symbolCross + openDate + openPrice + closePrice + profit + duration + interval

    with client:
        return client.loop.run_until_complete(client.send_message(my_channel, message))


