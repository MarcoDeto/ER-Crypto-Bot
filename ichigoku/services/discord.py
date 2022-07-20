from discord import Webhook, RequestsWebhookAdapter

ichigoku_channel = Webhook.partial(999460525756907531, 'LbM1pBqC0NUlvHiePsWkbd6XnyOiu8YRyEwGygwc19AXYK398hpDBCvfd_jC1rPJMKQ4', adapter=RequestsWebhookAdapter())

def sendDiscordMessage(message):
    ichigoku_channel.send(message, username='Er Crypto')
