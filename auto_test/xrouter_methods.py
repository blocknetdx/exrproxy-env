import os
import sys
import argparse
import json
import requests


def main(url: str, methods: list):
    for method in methods:
        payload = methods[method]

        try:
            response = requests.post(url+method, json=payload)
            if response.status_code == 401:
                raise SystemExit('Authorization error')
            if response.status_code == 403:
                raise SystemExit('Forbidden')

            code = response.status_code
            data = response.json()

            print('----------------------------------------')
            print(f'Method {method} HTTP status code {code}')
            print(data)
            print('\n')

        except requests.exceptions.RequestException as e:
            raise SystemExit(e)


if __name__ == '__main__':
    my_parser = argparse.ArgumentParser(description='SNODE RPC generator. Sends JSON-RPC requests.')

    my_parser.add_argument('Token',
                           metavar='token',
                           type=str,
                           help='Token. BLOCK, BTC, LTC, etc. ')

    my_parser.add_argument('Socket',
                           metavar='socket',
                           type=str,
                           help='HTTP socket, IP and port')

    my_parser.add_argument('Methods',
                           metavar='methods',
                           type=str,
                           help='file of RPC methods')

    args = my_parser.parse_args()

    http_socket = args.Socket
    rpc_methods = args.Methods
    token = args.Token
    if not os.path.isfile(rpc_methods):
        print('The file specified does not exist')
        sys.exit()

    with open(rpc_methods) as json_file:
        methods = json.load(json_file)['methods']
    url = http_socket + '/xr/' + token + '/'
    main(url, methods)
