import unittest
import requests
import json


class Connect:

    def __init__(self, http_socket: str, rpc_user: str, rpc_password: str):
        self._TARGET = http_socket
        self._USER = rpc_user
        self._PASSWORD = rpc_password

    def json_rpc(self, method: str, params=None):
        if params:
            payload = {'method': method,
                       'params': params}
        else:
            payload = {'method': method}

        try:
            response = requests.post(self._TARGET, json=payload, auth=(self._USER, self._PASSWORD))
            if response.status_code == 401:
                raise SystemExit('Authorization error')
            if response.status_code == 403:
                raise SystemExit('Forbidden')
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

        return response


class TestMethods(unittest.TestCase):

    def test_dxgetlocaltokens(self):
        response = self.req.json_rpc('dxgetlocaltokens')
        data = response.json()
        self.assertEqual(data['result'], self.template['dxgetlocaltokens'])

    def test_dxgettokenbalances(self):
        response = self.req.json_rpc('dxgettokenbalances')
        data = response.json()
        self.assertEqual(data['result'], self.template['dxgettokenbalances'])

    def test_servicenodestatus(self):
        response = self.req.json_rpc('servicenodestatus')
        data = response.json()
        if data['result']:
            data = {'status': data['result']['status'], 'services': data['result']['services']}
        self.assertEqual(data, self.template['servicenodestatus'])

    def test_dxgetutxos(self):
        response = self.req.json_rpc('dxgetutxos', ['BTC'])
        data = response.json()
        self.assertEqual(data['result'], self.template['dxgetutxos'])


if __name__ == '__main__':

    target = 'http://127.0.0.1:41414'
    user = 'user'
    password = 'pass'

    with open('template.json') as json_file:
        TestMethods.template = json.load(json_file)

    TestMethods.req = Connect(target, user, password)
    unittest.main()
