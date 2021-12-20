import json
import requests
import argparse

query = """
query MyQuery {
  xquery(where: {xquery_chain_name: {_eq: "AVAX"}, xquery_query_name: {_eq: "Swap"}}, limit: 10) {
    xquery_sender
    xquery_amount0in
    xquery_amount1in
    xquery_amount0out
    xquery_amount1out
    xquery_to
    xquery_token1_symbol
    xquery_token1_name
    xquery_token1_decimals
    xquery_token0_symbol
    xquery_token0_name
    xquery_token0_decimals
    xquery_blocknumber
    xquery_timestamp
  }
}"""

parser = argparse.ArgumentParser()
parser.add_argument('--host', help='host of exrpoxy-env', default='127.0.0.1:80')
parser.add_argument('--projectid', help='project id', default=False)
parser.add_argument('--apikey', help='api-key', default=False)
parser.add_argument('--query', help='string of query', default=query)

args = parser.parse_args()
HOST = args.host
PROJECTID = args.projectid
APIKEY = args.apikey
QUERY = args.query

def run_query(host, query, project_id, api_key):
    headers = {'Api-Key':f'{api_key}'}
    request = requests.post(f'http://{host}/xrs/xquery/{project_id}/indexer/', headers=headers, json={'query': query})
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))

if __name__ == '__main__':
    if PROJECTID and APIKEY:
        results = run_query(HOST, QUERY, PROJECTID, APIKEY)
        print(results)
    else:
        print("Missing PROJECTID and/or APIKEY")