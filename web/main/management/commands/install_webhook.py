from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import telebot


class Command(BaseCommand):
    help = 'install webhook'

    def handle(self, *args, **options):
        bot = telebot.TeleBot(settings.TELEGRAM_BOT_API)
        webhook_url = "https://{host}:{port}/{path}".format(
            host=settings.DOMAIN,
            port=settings.SITE_SSL_PORT,
            path=settings.TELEGRAM_WEBHOOK_PATH
        )
        resp = bot.set_webhook(
            url=webhook_url,
            certificate=open(settings.PUBLIC_SSL_CERT, 'r')
        )
        if resp:
            self.stdout.write(self.style.SUCCESS('Webhook was set to {}'.format(webhook_url)))
        else:
            self.stdout.write(self.style.WARNING('Some shit hapened! resp: {}'.format(resp)))