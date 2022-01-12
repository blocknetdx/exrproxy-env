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
    xquery_tx_hash
  }
}"""

def run_help(host, project_id):
    request = requests.post(f'http://{host}/xrs/xquery/{project_id}/help')
    if request.status_code == 200:
        return request.text
    else:
        raise Exception("XQuery help failed to run by returning code of {}".format(request.status_code))

def run_query(host, query, project_id, api_key):
    headers = {'Api-Key':f'{api_key}'}
    request = requests.post(f'http://{host}/xrs/xquery/{project_id}/indexer/', headers=headers, json={'query': query})
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("XQuery call failed to run by returning code of {}".format(request.status_code))

def run_get_graph(host, project_id):
    request = requests.post(f'http://{host}/xrs/xquery/{project_id}/help/graph')
    if request.status_code == 200:
        return request.json()
    else:
        print(request.text)
        raise Exception("XQuery current graph failed to run by returning code of {}".format(request.status_code))

def run_get_schema(host, project_id):
    request = requests.post(f'http://{host}/xrs/xquery/{project_id}/help/schema')
    if request.status_code == 200:
        return request.text
    else:
        print(request.text)
        raise Exception("XQuery schema failed to run by returning code of {}".format(request.status_code))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', help='Host of EXR', default='127.0.0.1:80')
    parser.add_argument('--projectid', help='ID of EXR project', default=False)
    parser.add_argument('--apikey', help='API-KEY of EXR project', default=False)
    parser.add_argument('--query', help='Query string', default=query)
    parser.add_argument('--xqhelp', help='Display XQuery help message', action='store_true')
    parser.add_argument('--xqgraph', help='Display XQuery current graph', action='store_true')
    parser.add_argument('--xqschema', help='Display XQuery schema', action='store_true')

    args = parser.parse_args()
    HOST = args.host
    PROJECTID = args.projectid
    APIKEY = args.apikey
    QUERY = args.query
    XQHELP = args.xqhelp
    XQGRAPH = args.xqgraph
    XQSCHEMA = args.xqschema

    
    if PROJECTID and APIKEY:
        results = run_query(HOST, QUERY, PROJECTID, APIKEY)
        print("#### XQuery query")
        print(results)
    elif XQHELP and PROJECTID:
        results = run_help(HOST, PROJECTID)
        print("#### XQuery help")
        print(results)
    elif XQGRAPH and PROJECTID:
        results = run_get_graph(HOST, PROJECTID)
        print("#### XQuery current graph")
        print(results)
    elif XQSCHEMA and PROJECTID:
        results = run_get_schema(HOST, PROJECTID)
        print("#### XQuery schema")
        print(results)
    else:
        print("Missing PROJECTID and/or APIKEY")
        parser.print_help()