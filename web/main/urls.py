from django.conf.urls import url
from django.conf import settings

from . import views

urlpatterns = [
    url(r'^{0}$'.format(settings.TELEGRAM_WEBHOOK_PATH), views.telegram_webhook),
    url(r'^zabbix_callback/(?P<token>\w{50,100})$', views.zabbix_callback),
    url(r'', views.main),
]
