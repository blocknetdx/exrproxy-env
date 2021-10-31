import unittest
import requests


class Connect:

    def __init__(self, http_socket: str):
        self._TARGET = http_socket

    def json_rpc(self, url: str, method: str, params=None):
        if params:
            payload = {'method': method,
                       'params': params,
                       'jsonrpc': '2.0',
                       'id': 1}
        else:
            payload = {'method': method}

        try:
            response = requests.post(self._TARGET+url, json=payload)
            if response.status_code == 401:
                raise SystemExit('Authorization error')
            if response.status_code == 403:
                raise SystemExit('Forbidden')
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

        return response


class TestMethods(unittest.TestCase):

    def test_getBlockchainID(self):
        url = '/ext/info'
        method = 'info.getBlockchainID'
        chains = ['X', 'P', 'C']
        for chain in chains:
            params = {"alias": chain}
            response = self.req.json_rpc(url, method, params)
            data = response.json()
            blockchain_id = data['result']['blockchainID']
            print(f'Chain {chain}, blockchain id = {blockchain_id}')
            self.assertEqual(type(blockchain_id), str)

    def test_getContainerByIndex(self):
        method = 'index.getContainerByIndex'
        params = {"index": 0, "encoding": "hex"}
        chains = ['X/tx', 'P/block']
        for chain in chains:
            url = f'/ext/index/{chain}'
            response = self.req.json_rpc(url, method, params)
            data = response.json()
            container_id = data['result']['id']
            print(f'Chain {chain},index 0, container id = {container_id}')
            self.assertEqual(type(container_id), str)


if __name__ == '__main__':

    target = 'http://127.0.0.1/xrs/xquery'
    TestMethods.req = Connect(target)
    unittest.main()
