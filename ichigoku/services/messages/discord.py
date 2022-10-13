from discord import Webhook, RequestsWebhookAdapter # pip install discord.py==1.7.3 ### AND ### # pip install discord-webhook

ichigoku_channel = Webhook.partial(1000139269161107628, 'DndlL8LkxBEOtg_yZhKj1s7ssfiaN0s6mvL_tmOh4qow0Xqy8vQjtgrij9HoCm2qSbky', adapter=RequestsWebhookAdapter())

def sendDiscordMessage(message):
    ichigoku_channel.send(message, username='Er Crypto')

'''
import requests
from discord import SyncWebhook # Import SyncWebhook

webhook = SyncWebhook.from_url('https://discord.com/api/webhooks/[my-webhook]') # Initializing webhook
webhook.send(content="Hello World") # Executing webhook.
'''