import logging
from collections import namedtuple

import telebot
from django.conf import settings
from requests.exceptions import RequestException

from api_action import RPCException, ZabbixApi
from . import constants as c
from . import models

LOGGER = logging.getLogger(__name__)
Command = namedtuple('Command', ['command', 'handler', 'help'])


class TelegramZabbixBot:
    def __init__(self, api):
        self.api = api
        self.command_list = [
            Command('/help', self.help, '/help'),
            Command('/register', self.register, '/register <zabbix_server_ip> <zabbix_user> '
                                                '<zabbix_password>'),
            Command('/stop', self.stop, '/stop - deleting you from the system'),
            Command('/hosts', self.hosts, '/hosts - getting list of hosts from zabbix'),
            Command('/items', self.items, '/items <host_id> - getting list of registered items '
                                          'for host'),
            Command('/last_value', self.last_value, '/last_value <item_id> - getting item last '
                                                    'value')
        ]

        self.commands = {x.command: x for x in self.command_list}

    def handle_update(self, update):
        if update.message is not None:
            self.handle_message(update.message)

    def handle_message(self, message):
        user, created = models.User.objects.get_or_create(telegram_id=message.from_user.id)
        if created:
            self.api.send_message(message.from_user.id, c.HELLO_MESSAGE)
        else:
            command = self._find_command(message.text or '')
            if command is None:
                self.help(user, message)
            else:
                command.handler(user, message)

    def _find_command(self, text):
        args = text.split()
        if '@' in args[0]:
            args[0] = args[0][:args[0].index('@')]

        if args[0] in self.commands:
            return self.commands[args[0]]
        return None

    def help(self, user, message):
        available_commands = '\n\t'.join(c.help for c in self.command_list)
        self.api.send_message(user.telegram_id, "Available commands:\n\t{}".format(available_commands))

    def register(self, user, message):
        args = (message.text or '').split()
        if len(args) != 4:
            self.api.send_message(user.telegram_id, self.commands['/register'].help)
            return

        user.zabbix_host = args[1]
        user.zabbix_user = args[2]
        user.zabbix_pass = args[3]
        self.api.send_message(user.telegram_id, "Ok. Trying to create an action.")
        try:
            command = "curl -k --data '{{TRIGGER.NAME}}' {callback}".format(
                callback=user.get_zabbix_callback())
            api = ZabbixApi(user.zabbix_host, user.zabbix_user, user.zabbix_pass)
            if api.create_action(command):
                self.api.send_message(user.telegram_id, "Action was successfully created.")
            else:
                self.api.send_message(user.telegram_id, "Action already registered.")
            user.save()
        except RPCException as ex:
            self.api.send_message(user.telegram_id, "Can't create action because of the reason: "
                                                    "{0}".format(ex.message))
        except RequestException:
            self.api.send_message(user.telegram_id, "Can't reach zabbix. Are you sure that it is "
                                                    "available?")
        except Exception as ex:
            LOGGER.exception(ex)
            self.api.send_message(user.telegram_id, "Can't create action. Are you sure that your "
                                                    "credentials a real?")

    def stop(self, user, message):
        user.delete()
        self.api.send_message(user.telegram_id, c.U_WAS_DELETED)

    def hosts(self, user, message):
        if user.zabbix_host is None:
            self.api.send_message(user.telegram_id, "You are not registered. Register yourself "
                                                    "using command /register")
            return
        try:
            api = ZabbixApi(user.zabbix_host, user.zabbix_user, user.zabbix_pass)
            hosts = api.get_hosts()
            text = self._list_of_dict_to_str(hosts)
            self.api.send_message(user.telegram_id, text)
        except RPCException as ex:
            self.api.send_message(user.telegram_id, "Can't perform an action at zabbix because of "
                                                    "the reason: {0}".format(ex.message))
        except RequestException:
            self.api.send_message(user.telegram_id, "Can't reach zabbix. Are you sure that it is "
                                                    "available?")
        except Exception as ex:
            LOGGER.exception(ex)
            self.api.send_message(user.telegram_id, "Can't perform an action at zabbix.")

    def items(self, user, message):
        if user.zabbix_host is None:
            self.api.send_message(user.telegram_id, "You are not registered. Register yourself "
                                                    "using command /register")
            return
        args = (message.text or '').split()
        if len(args) != 2:
            self.api.send_message(user.telegram_id, self.commands['/items'].help)
            return

        try:
            api = ZabbixApi(user.zabbix_host, user.zabbix_user, user.zabbix_pass)
            items = api.get_items(args[1])
            text = self._list_of_dict_to_str(items)
            self.api.send_message(user.telegram_id, text)
        except RPCException as ex:
            self.api.send_message(user.telegram_id, "Can't perform an action at zabbix because of "
                                                    "the reason: {0}".format(ex.message))
        except RequestException:
            self.api.send_message(user.telegram_id, "Can't reach zabbix. Are you sure that it is "
                                                    "available?")
        except Exception as ex:
            LOGGER.exception(ex)
            self.api.send_message(user.telegram_id, "Can't perform an action at zabbix.")

    def last_value(self, user, message):
        if user.zabbix_host is None:
            self.api.send_message(user.telegram_id, "You are not registered. Register yourself "
                                                    "using command /register")
            return
        args = (message.text or '').split()
        if len(args) != 2:
            self.api.send_message(user.telegram_id, self.commands['/last_value'].help)
            return

        try:
            api = ZabbixApi(user.zabbix_host, user.zabbix_user, user.zabbix_pass)
            item = api.get_item_last_value(args[1])
            text = self._list_of_dict_to_str([item])
            self.api.send_message(user.telegram_id, text)
        except RPCException as ex:
            self.api.send_message(user.telegram_id, "Can't perform an action at zabbix because of "
                                                    "the reason: {0}".format(ex.message))
        except RequestException:
            self.api.send_message(user.telegram_id, "Can't reach zabbix. Are you sure that it is "
                                                    "available?")
        except Exception as ex:
            LOGGER.exception(ex)
            self.api.send_message(user.telegram_id, "Can't perform an action at zabbix.")

    def _list_of_dict_to_str(self, items):
        text_list = []
        for item in items:
            item_text = '\n'.join("{0}: {1}".format(key, value) for key, value in item.items())
            text_list.append(item_text)
        return '\n\n====================\n\n'.join(text_list)



class TelegramApi(telebot.TeleBot):
    def send_message(self, chat_id, text, *args, **kwargs):
        splitted_text = telebot.util.split_string(text, 3000)
        for text in splitted_text:
            super().send_message(chat_id, text, *args, **kwargs)


api = TelegramApi(settings.TELEGRAM_BOT_API)
bot = TelegramZabbixBot(api)
