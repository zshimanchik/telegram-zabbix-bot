
#  curl https://api.telegram.org/bot133216541:AAEsCwSzhEDdrr8rTo4FQ3FWHE6TlL83j_c/sendMessage -d 'chat_id=126881502' -d 'text=Hello, world'

import requests

zabbix_url = "http://localhost/api_jsonrpc.php"


class RCPException(Exception):
    def __init__(self, code, message):
        self.code = code
        self.message = message

    @staticmethod
    def from_dict(data):
        return RCPException(data.get('code'), data.get('message'))


def make_data(method, params=None, auth=None):
    return {
        'jsonrpc': '2.0',
        'id': 123,
        'method': method,
        'auth': auth,
        'params': params or {},
    }


def rpc(method, params=None, auth=None):
    data = make_data(method, params, auth)
    response = requests.post(zabbix_url, json=data)
    response.raise_for_status()
    resp = response.json()
    if 'error' in resp:
        raise RCPException.from_dict(resp['error'])
    return resp['result']

token = rpc('user.login', {'user': 'Admin', 'password': 'zabbix'})

create_action_data = {
    "esc_period": "60",
    "eventsource": 0,
    "name": "Notify Telegram Bot",
    "operations": [
        {
            "operationtype": 1,
            'opcommand': {
                # 'command': 'curl http://potatolol.requestcatcher.com/ --data "{TRIGGER.STATUS}: {TRIGGER.NAME}"',
                'command': "curl https://api.telegram.org/bot133216541:AAEsCwSzhEDdrr8rTo4FQ3FWHE6TlL83j_c/sendMessage -d 'chat_id=126881502' -d 'text={TRIGGER.NAME}'",
                'type': 0,
                'execute_on': 1,
            },
            'opcommand_hst': [
                {
                    'hostid': 0
                },
            ],
        },
    ],
    'def_longdata': '{TRIGGER.STATUS}: {TRIGGER.NAME}',
    'def_shortdata': '{TRIGGER.STATUS}: {TRIGGER.NAME}',
}

rpc('action.create', create_action_data, token)


