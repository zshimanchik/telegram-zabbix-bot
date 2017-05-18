import telebot
from django.conf import settings


class TelegramZabbixBot:
    def __init__(self, api):
        self.api = api

    def handle_update(self, update):
        if update.message is not None:
            self.handle_message(update.message)

    def handle_message(self, message):
        self.api.send_message(message.from_user.id, "Hello =)")


api = telebot.TeleBot(settings.TELEGRAM_BOT_API)
bot = TelegramZabbixBot(api)
