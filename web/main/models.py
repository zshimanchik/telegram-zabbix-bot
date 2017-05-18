from django.db import models
import random
import string


def token_generator():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(90))


class User(models.Model):
    telegram_id = models.CharField(max_length=30, null=False, blank=False)
    zabbix_host = models.CharField(max_length=100, null=True, blank=True)
    zabbix_user = models.CharField(max_length=100, null=True, blank=True)
    zabbix_pass = models.CharField(max_length=100, null=True, blank=True)
    token = models.CharField(max_length=100, default=token_generator, null=False, blank=False)

    def __str__(self):
        return "User[{0}]".format(self.telegram_id)
