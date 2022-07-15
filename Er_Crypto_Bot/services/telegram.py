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


import json
from datetime import date, datetime

from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.messages import (GetHistoryRequest)
from telethon.tl.types import (
    PeerChannel
)

TELEGRAM_TOKEN = "5554013164:AAEaxjGrj2KHUbGuSz9MCH4aeKGcy7c28Ao"


# some functions to parse json date
class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()

        if isinstance(o, bytes):
            return list(o)

        return json.JSONEncoder.default(self, o)


# Reading Configs

# Setting configuration values
api_id = 18943005
api_hash = '15b0d68a8f31361f902ddd4f11c30d1f'

api_hash = str(api_hash)

phone = "+39 3342927723"
username =  "blingus"

# Create the client and connect
client = TelegramClient(username, api_id, api_hash)

async def main(phone):
    await client.start()
    print("Client Created")
    # Ensure you're authorized
    if await client.is_user_authorized() == False:
        await client.send_code_request(phone)
        try:
            await client.sign_in(phone, input('Enter the code: '))
        except SessionPasswordNeededError:
            await client.sign_in(password=input('Password: '))

    me = await client.get_me()

    my_channel = await client.get_entity("https://t.me/ercryptobotto")

    test = await client.send_message(my_channel, "message test")


with client:
    client.loop.run_until_complete(main(phone))


