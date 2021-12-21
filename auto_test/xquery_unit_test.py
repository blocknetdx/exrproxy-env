import json
import requests
import argparse
import sys


def main(host, project_id):
    try:
        response = requests.post(f'http://{host}/xrs/xquery/{project_id}/help')
        if response.status_code == 401:
            raise SystemExit('Authorization error')
        if response.status_code == 403:
            raise SystemExit('Forbidden')

        code = response.status_code
        data = response.text

        print('----------------------------------------')
        print(f'XQuery Help HTTP status code {code}\n')
        print(data)
        print('\n')

    except requests.exceptions.RequestException as e:
        raise SystemExit(e)

    try:
        response = requests.post(f'http://{host}/xrs/xquery/{project_id}/help/graph')
        if response.status_code == 401:
            raise SystemExit('Authorization error')
        if response.status_code == 403:
            raise SystemExit('Forbidden')

        code = response.status_code
        data = response.text

        print('----------------------------------------')
        print(f'XQuery Current Graph HTTP status code {code}\n')
        print(data)
        print('\n')

    except requests.exceptions.RequestException as e:
            raise SystemExit(e)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='XQuery tester. Checks for help and current graph')
    parser.add_argument('--projectid', help='ID of EXR project', default=False)

    args = parser.parse_args()
    HOST = '185.217.127.108:80'
    PROJECTID = args.projectid
    
    if PROJECTID:
        results = main(HOST, PROJECTID)
    else:
        print("Missing PROJECTID")
        parser.print_help()
        sys.exit()