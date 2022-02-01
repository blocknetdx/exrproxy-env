import json
import requests
import argparse
from string import Template

schema = """
  id
  xquery_chain_name
  xquery_query_name
  xquery_timestamp
  xquery_tx_hash
  xquery_token0_name
  xquery_token0_symbol
  xquery_token0_decimals
  xquery_token1_name
  xquery_token1_symbol
  xquery_token1_decimals
  xquery_side
  xquery_address_filter
  xquery_blocknumber
  xquery_fn_name
  xquery_from
  xquery_to
  xquery_value
  xquery_src
  xquery_wad
  xquery_dst
  xquery_owner
  xquery_spender
  xquery_sender
  xquery_amount0
  xquery_amount1
  xquery_amount0in
  xquery_amount1in
  xquery_amount0out
  xquery_amount1out
  xquery_reserve0
  xquery_reserve1
  xquery_none
  xquery_deadline
  xquery_v
  xquery_r
  xquery_s
  xquery_data
  xquery_params
  xquery_token
  xquery_nonce
  xquery_expiry
  xquery_amountminimum
  xquery_recipient
  xquery_feebips
  xquery_feerecipient
  xquery_amount0delta
  xquery_amount1delta
  xquery_tokena
  xquery_tokenb
  xquery_amountadesired
  xquery_amountbdesired
  xquery_amountamin
  xquery_amountbmin
  xquery_amounttokendesired
  xquery_amounttokenmin
  xquery_amountavaxmin
  xquery_amountout
  xquery_reservein
  xquery_reserveout
  xquery_amountin
  xquery_path
  xquery_amounta
  xquery_reservea
  xquery_reserveb
  xquery_liquidity
  xquery_approvemax
  xquery_amountoutmin
  xquery_amountinmax
"""

query = Template("""
query MyQuery {
  xquery(where: {xquery_chain_name: {_eq: "AVAX"}, xquery_query_name: {_eq: "Swap"} }, limit: 20) {
  $schema
  }
}""").substitute(schema=schema)

def xpair_query(pairs, limit=20):
    pair_filter = []
    for pair in pairs:
        pair_filter.append(Template("""{xquery_token0_symbol: {_regex: "$token0"}, xquery_token1_symbol: {_regex: "$token1"} }""").substitute(token0=pair[0],token1=pair[1]))
        pair_filter.append(Template("""{xquery_token0_symbol: {_regex: "$token0"}, xquery_token1_symbol: {_regex: "$token1"} }""").substitute(token0=pair[1],token1=pair[0]))
    template = Template("""
    query XPair {
      xquery(where: {
    _or: [
      $combo
    ], 
  }, limit: $limit) {
    $schema
    }
}""").substitute(combo=','.join(pair_filter), schema=schema, limit=limit)
    return template

def xfilter_query(routers, limit=20):
    router_names = []
    for router in routers:
        router_names.append(Template("""{xquery_address_filter: {_regex: "$router"} }""").substitute(router=router))
    return Tempalte("""
    query XAddressFilter {
      xquery(where: {
    _or: [
      $combo
    ], 
  }, limit: $limit) {
    $schema
    }
}""").substitute(combo=','.join(router_names), schema=schema, limit=limit)


def xpair_filter_query(pairs, routers, limit=20):
    combos = []
    for router in routers:
        c = []
        c.append(Template("""xquery_address_filter: {_regex: "$router"}""").substitute(router=router))
        for pair in pairs:
            c.append(Template("""xquery_token0_symbol: {_regex: "$token0"}, xquery_token1_symbol: {_regex: "$token1"}""").substitute(token0=pair[0],token1=pair[1]))
            c.append(Template("""xquery_token0_symbol: {_regex: "$token0"}, xquery_token1_symbol: {_regex: "$token1"}""").substitute(token0=pair[1],token1=pair[0]))
        c = ','.join(c)
        c = '{'+c+'}'
        combos.append(c)
    return Tempalte("""
    query XPairXAddressFilter {
      xquery(where: {
    _or: [
      $combo
    ], 
  }, limit: $limit) {
    $schema
    }
}""").substitute(combo=','.join(combos), schema=schema, limit=limit)

def xaddress(addresses, limit=20):
    c = []
    for address in addresses:
        c.append(Template("""{xquery_to: {_regex: "$address"} }""").substitute(address=address))
        c.append(Template("""{xquery_sender: {_regex: "$address"} }""").substitute(address=address))
        c.append(Template("""{xquery_from: {_regex: "$address"} }""").substitute(address=address))
        c.append(Template("""{xquery_spender: {_regex: "$address"} }""").substitute(address=address))
        c.append(Template("""{xquery_recipient: {_regex: "$address"} }""").substitute(address=address))
        c.append(Template("""{xquery_path: {_regex: "$address"} }""").substitute(address=address))
        c.append(Template("""{xquery_owner: {_regex: "$address"} }""").substitute(address=address))
    return Template("""
    query XAddress {
      xquery(where: {
    _or: [
      $combo
    ], 
  }, limit: $limit) {
    $schema
    }
}""").substitute(combo=','.join(c), schema=schema, limit=limit)


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
    parser.add_argument('--xquery', help='Query string', default=query)
    parser.add_argument('--xqhelp', help='Display XQuery help message', action='store_true')
    parser.add_argument('--xqgraph', help='Display XQuery current graph', action='store_true')
    parser.add_argument('--xqschema', help='Display XQuery schema', action='store_true')
    parser.add_argument('--xqaddress', help='Address to query for', nargs='*')
    parser.add_argument('--xqpair', help='Pairs to query for | USDC/USDT ETH/USDT', nargs='*')
    parser.add_argument('--xqrouter', help='Routers names to query for | Uniswap Pangolin', nargs='*')

    args = parser.parse_args()
    HOST = args.host
    PROJECTID = args.projectid
    APIKEY = args.apikey
    XQUERY = args.xquery
    XQHELP = args.xqhelp
    XQGRAPH = args.xqgraph
    XQSCHEMA = args.xqschema

    if PROJECTID and APIKEY:
        results = run_query(HOST, XQUERY, PROJECTID, APIKEY)
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