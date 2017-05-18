import json

import telebot
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import logging

from .bot import bot

LOGGER = logging.getLogger(__name__)


@csrf_exempt
def telegram_webhook(request):
    try:
        data = request.body.decode('utf8')
        update_dict = json.dumps(json.loads(data), ensure_ascii=False)
        LOGGER.debug('got update={}'.format(update_dict))
        update = telebot.types.Update.de_json(request.body.decode('utf8'))
        bot.handle_update(update)
    except Exception as ex:
        LOGGER.exception("exception during handling telegram webhook, with data: %s",
                         request.body,
                         exc_info=ex)
    return HttpResponse()


def main(request):
    LOGGER.info("MAINNNN")
    return HttpResponse(b"Hi, this is main page")
