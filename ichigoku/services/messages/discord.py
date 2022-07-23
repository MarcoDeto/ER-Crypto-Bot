from discord import Webhook, RequestsWebhookAdapter

ichigoku_channel = Webhook.partial(1000139269161107628, 'DndlL8LkxBEOtg_yZhKj1s7ssfiaN0s6mvL_tmOh4qow0Xqy8vQjtgrij9HoCm2qSbky', adapter=RequestsWebhookAdapter())

def sendDiscordMessage(message):
    ichigoku_channel.send(message, username='Er Crypto')
