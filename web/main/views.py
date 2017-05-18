import json

import telebot
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import logging

from .bot import bot
from . import models

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


@csrf_exempt
def zabbix_callback(request, token):
    try:
        user = models.User.objects.get(token=token)
        if request.body:
            LOGGER.debug("Zabbix callback: for user {0}, "
                         "sending data: \'{1}\'".format(user, request.body))
            bot.api.send_message(user.telegram_id, request.body)
        return HttpResponse("Zabbix callback... <br>"
                            "for user: {}<br>"
                            "sending data: {}".format(user, request.body))
    except models.User.DoesNotExist:
        return HttpResponse("Zabbix callback. User not found with token: {}".format(token),
                            status=404)


def main(request):
    LOGGER.info("MAINNNN")
    return HttpResponse(b"Hi, this is main page")
