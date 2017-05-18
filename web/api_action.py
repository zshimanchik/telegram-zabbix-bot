import requests


class RPCException(Exception):
    def __init__(self, code, message):
        self.code = code
        self.message = message

    @staticmethod
    def from_dict(data):
        return RPCException(data.get('code'), data.get('message'))


def make_data(method, params=None, auth=None):
    return {
        'jsonrpc': '2.0',
        'id': 123,
        'method': method,
        'auth': auth,
        'params': params or {},
    }


def rpc(zabbix_url, method, params=None, auth=None):
    data = make_data(method, params, auth)
    response = requests.post(zabbix_url, json=data)
    response.raise_for_status()
    resp = response.json()
    if 'error' in resp:
        raise RPCException.from_dict(resp['error'])
    return resp['result']


def create_action(zabbix_server, user, password, command):
    zabbix_url = 'http://{}/api_jsonrpc.php'.format(zabbix_server)
    token = rpc(zabbix_url, 'user.login', {'user': user, 'password': password})

    create_action_data = {
        "esc_period": "60",
        "eventsource": 0,
        "name": "Notify Telegram Bot",
        "operations": [
            {
                "operationtype": 1,
                'opcommand': {
                    'command': command,
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

    rpc(zabbix_url, 'action.create', create_action_data, token)
