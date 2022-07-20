from discord import Webhook, RequestsWebhookAdapter

webhook = Webhook.partial(999117023760093224, 'kM1MVQrWbn6g8E-UiU6LKT_kkgUuAXRCX0lSNZBN37hpkFerg3VqhH1gftXJILzCSQvm', adapter=RequestsWebhookAdapter())


def sendDiscordMessage(message):
    webhook.send(message, username='Er Crypto')
