import requests
import time


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


def login(zabbix_url, user, password):
    return rpc(zabbix_url, 'user.login', {'user': user, 'password': password})


class ZabbixApi:
    def __init__(self, zabbix_url, user, password):
        self._url = 'http://{}/api_jsonrpc.php'.format(zabbix_url)
        self._token = login(self._url, user, password)

    def create_action(self, command):
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

        rpc(self._url, 'action.create', create_action_data, self._token)

    def get_hosts(self):
        return rpc(self._url, 'host.get', {'output': ['name', 'host', 'hostid']}, self._token)

    def get_items(self, host_id):
        params = {'hostids': [host_id], 'output': ['itemid', 'name', 'key_']}
        return rpc(self._url, 'item.get', params, self._token)

    def get_item_last_value(self, item_id):
        params = {'itemids': [item_id], 'output': ['lastclock', 'lastvalue']}
        item = rpc(self._url, 'item.get', params, self._token)[0]
        t = time.localtime(int(item.pop('lastclock')))
        item['lastcheck'] = time.strftime('%Y-%m-%d %H:%M:%S', t)
        return item
