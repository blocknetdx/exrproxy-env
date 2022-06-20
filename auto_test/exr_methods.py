import os
import sys
import argparse
import json
import requests


def main(url: str, methods: list, API_Key: str):
    for method in methods:
        payload = {'method': method,
                   'params': methods[method]
                   }
        headers = {"Content-Type": "application/json",
                   "Api-Key": API_Key}
        try:
            response = requests.post(url, json=payload, headers=headers)

            if response.status_code == 401:
                raise SystemExit('Authorization error', response.json())
            if response.status_code == 403:
                raise SystemExit('Forbidden', response.json())
            if response.status_code == 404:
                raise SystemExit('404 error', response.json())

            code = response.status_code
            data = response.json()
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

        if data:
            if 'result' in data:
                print('---------------------------------------')
                print(url)
                print(f'Method {method} HTTP status code {code}')
                if type(data['result']) == dict:
                    for i in data['result']:
                        print(i, ':', data['result'][i])
                else:
                    print(data['result'])
                print('\n')
            else:
                print('---------------------------------------')
                print(url)
                print(f'Method {method} HTTP status code {code}')
                for i in data:
                    print(i, ':', data[i])
                print('\n')


if __name__ == '__main__':
    my_parser = argparse.ArgumentParser(description='EXR RPC generator. Sends JSON-RPC requests.')

    subparser = my_parser.add_subparsers(dest='command')
    create_project = subparser.add_parser('new_project')
    existing_project = subparser.add_parser('project')

    existing_project.add_argument('--api-key', type=str, help='API key used to send request EXR', required=True)
    existing_project.add_argument('--project-id', type=str, help='ID of EXR project', required=True)

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

    if not os.path.isfile(rpc_methods):
        print('The file specified does not exist')
        sys.exit()

    with open(rpc_methods) as json_file:
        data = json.load(json_file)

    methods = data['methods']
    

    API_Key = None
    project_id = None

    if args.command == 'project':
        API_Key = args.api_key
        project_id = args.project_id
        chains = ['AVAX','ETH', 'SYS']
        for chain in chains:
            if chain =='ETH':
                url = http_socket + '/xrs/evm_passthrough'+f'/{chain}'+f'/{project_id}'
            elif chain =='SYS':
                url = http_socket + '/xrs/evm_passthrough'+f'/{chain}'+f'/{project_id}'
            elif chain =='AVAX':
                url = http_socket + '/xrs/evm_passthrough'+f'/{chain}'+f'/{project_id}'+'/ext/bc/C/rpc'
            main(url, methods, API_Key)

    elif args.command == 'new_project':
        url = http_socket + '/xrs/projects'
        methods = {'request_project': []}
        main(url, methods, API_Key)

    
