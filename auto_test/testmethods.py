import os
import sys
import argparse
import json
import requests


def main(http_socket: str, rpc_user: str, rpc_password: str, methods: list):

    for method in methods:
        payload = {'method': method}
        try:
            response = requests.post(http_socket, json=payload, auth=(rpc_user, rpc_password))
            if response.status_code == 401:
                raise SystemExit('Authorization error')
            if response.status_code == 403:
                raise SystemExit('Forbidden')

            code = response.status_code
            data = response.json()
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

        if response:
            print(f'Method {method} HTTP status code {code}')
            print(data['result'], '\n')
        else:
            print(f'Method {method} HTTP status code {code}')
            print('RPC code error ', data['error']['code'])
            print(data['error']['message'], '\n')


if __name__ == '__main__':
    my_parser = argparse.ArgumentParser(description='SNODE RPC generator. Sends JSON-RPC requests.')

    my_parser.add_argument('Socket',
                           metavar='socket',
                           type=str,
                           help='HTTP socket, IP and port')
    my_parser.add_argument('RPCuser',
                           metavar='rpcuser',
                           type=str,
                           help='rpc username')
    my_parser.add_argument('RPCpassword',
                           metavar='rpcpassword',
                           type=str,
                           help='rpc password')

    my_parser.add_argument('Methods',
                           metavar='methods',
                           type=str,
                           help='file of RPC methods')

    args = my_parser.parse_args()

    http_socket = args.Socket
    rpc_user = args.RPCuser
    rpc_password = args.RPCpassword
    rpc_methods = args.Methods

    if not os.path.isfile(rpc_methods):
        print('The file specified does not exist')
        sys.exit()

    with open(rpc_methods) as json_file:
        methods = json.load(json_file)['methods']

    main(http_socket, rpc_user, rpc_password, methods)
