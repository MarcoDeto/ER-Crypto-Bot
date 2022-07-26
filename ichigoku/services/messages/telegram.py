from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError

from config import TELEGRAM_API_HASH, TELEGRAM_API_ID, TELEGRAM_CHANNEL, TELEGRAM_PHONE, TELEGRAM_USERBNAME

client = TelegramClient(TELEGRAM_USERBNAME, TELEGRAM_API_ID, TELEGRAM_API_HASH)

def init_telegram():
    with client:
        client.loop.run_until_complete(get_access())


async def get_access():
    await client.start()
    print("Telegram Client Created")
    # Ensure you're authorized
    if await client.is_user_authorized() == False:
        await client.send_code_request(TELEGRAM_PHONE)
        try:
            await client.sign_in(TELEGRAM_PHONE, input('Enter the code: '))
        except SessionPasswordNeededError:
            await client.sign_in(password=input('Password: '))


def get_channel():
    with client:
        return client.loop.run_until_complete(client.get_entity(TELEGRAM_CHANNEL))
    

def sendTelegramMessage(telegram, message):  

    with client:
        return client.loop.run_until_complete(client.send_message(telegram, message))


