import json
import requests
import argparse
from string import Template
from rich import print

xrouter_emoticon = ":twisted_rightwards_arrows:"

def default_query(schema):
    return Template("""
    query MyQuery {
      xquery(order_by: {xquery_blocknumber: desc}, limit: 20) {
      $schema
      }
}""").substitute(schema=schema)

def xpair_query(pairs, schema, limit=20):
    pair_filter = []
    for pair in pairs:
        pair_filter.append(Template("""{xquery_token0_symbol: {_regex: "$token0"}, xquery_token1_symbol: {_regex: "$token1"} }""").substitute(token0=pair[0],token1=pair[1]))
        pair_filter.append(Template("""{xquery_token0_symbol: {_regex: "$token0"}, xquery_token1_symbol: {_regex: "$token1"} }""").substitute(token0=pair[1],token1=pair[0]))
    template = Template("""
    query XPair {
      xquery(order_by: {xquery_blocknumber: desc}, where: {
    _or: [
      $combo
    ], 
  }, limit: $limit) {
    $schema
    }
}""").substitute(combo=','.join(pair_filter), schema=schema, limit=limit)
    return template

def xfilter_query(routers, schema, limit=20):
    router_names = []
    for router in routers:
        router_names.append(Template("""{xquery_address_filter: {_regex: "$router"} }""").substitute(router=router))
    return Template("""
    query XAddressFilter {
      xquery(order_by: {xquery_blocknumber: desc}, where: {
    _or: [
      $combo
    ], 
  }, limit: $limit) {
    $schema
    }
}""").substitute(combo=','.join(router_names), schema=schema, limit=limit)


def xpair_filter_query(pairs, routers, schema, limit=20):
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
    return Template("""
    query XPairXAddressFilter {
      xquery(order_by: {xquery_blocknumber: desc}, where: {
    _or: [
      $combo
    ], 
  }, limit: $limit) {
    $schema
    }
}""").substitute(combo=','.join(combos), schema=schema, limit=limit)

def xaddress_query(addresses, schema, limit=20):
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
      xquery(order_by: {xquery_blocknumber: desc}, where: {
    _or: [
      $combo
    ], 
  }, limit: $limit) {
    $schema
    }
}""").substitute(combo=','.join(c), schema=schema, limit=limit)

def xtx_query(txs_hash, schema):
    txs = []
    for tx in txs_hash:
        txs.append(Template("""{xquery_tx_hash: {_regex: "$tx"} }""").substitute(tx=tx))
    return Template("""
    query XTxs {
      xquery(order_by: {xquery_blocknumber: desc}, where: {
    _or: [
      $combo
    ], 
  }) {
    $schema
    }
}""").substitute(combo=','.join(txs), schema=schema)


def run_help(host, project_id):
    request = requests.post(f'http://{host}/xrs/xquery/{project_id}/help',timeout=300)
    if request.status_code == 200:
        return request.text
    else:
        print("XQuery help failed to run by returning code of {}".format(request.status_code))

def run_query(host, query, project_id, api_key):
    headers = {'Api-Key':f'{api_key}'}
    request = requests.post(f'http://{host}/xrs/xquery/{project_id}/indexer/', headers=headers, json={'query': query},timeout=300)
    if request.status_code == 200:
        return request.json()
    else:
        print("XQuery call failed to run by returning code of {}".format(request.status_code))

def run_get_graph(host, project_id):
    request = requests.post(f'http://{host}/xrs/xquery/{project_id}/help/graph',timeout=300)
    if request.status_code == 200:
        return request.json()
    else:
        print("XQuery current graph failed to run by returning code of {}".format(request.status_code))

def run_get_schema(host, project_id):
    request = requests.post(f'http://{host}/xrs/xquery/{project_id}/help/schema',timeout=300)
    if request.status_code == 200:
        return request.text
    else:
        print("XQuery schema failed to run by returning code of {}".format(request.status_code))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', help='Host of EXR', default='127.0.0.1:80')
    parser.add_argument('--projectid', help='ID of EXR project', default=False)
    parser.add_argument('--apikey', help='API-KEY of EXR project', default=False)
    parser.add_argument('--xquery', help='Query string', default=False)
    parser.add_argument('--xqhelp', help='Display XQuery help message', action='store_true')
    parser.add_argument('--xqgraph', help='Display XQuery current graph', action='store_true')
    parser.add_argument('--xqschema', help='Display XQuery schema', action='store_true')
    parser.add_argument('--xqaddress', help='Address to query for', nargs='*')
    parser.add_argument('--xqpair', help='Pairs to query for | USDC/USDT ETH/USDT', nargs='*')
    parser.add_argument('--xqrouter', help='Routers names to query for | Uniswap Pangolin', nargs='*')
    parser.add_argument('--xqtx', help='Query for TX', nargs='*')
    parser.add_argument('--xqlimit', help='Number of results', default=20)

    args = parser.parse_args()
    HOST = args.host
    PROJECTID = args.projectid
    APIKEY = args.apikey
    XQUERY = args.xquery
    XQHELP = args.xqhelp
    XQGRAPH = args.xqgraph
    XQSCHEMA = args.xqschema
    XQADDRESS = args.xqaddress
    XQPAIR = args.xqpair
    XQROUTER = args.xqrouter
    XQLIMIT = args.xqlimit
    XQTX = args.xqtx

    if HOST:
        if PROJECTID and APIKEY:
            schema = '\n'.join([x for x in [x.split(":")[0].strip() for x in run_get_schema(HOST, PROJECTID).split('{')[1].split('}')[0].split('\n')] if x!='' and x[0]!='_'])
            if XQPAIR and not XQROUTER:
                pairs = []
                for pair in XQPAIR:
                    if "/" not in pair or pair.count("/")!=1:
                        print(":x:",f"ignoring unknown format {pair}...")
                    else:
                        if XQPAIR.count(pair)==1:
                            p0 = pair.split("/")[0]
                            p1 = pair.split("/")[1]
                            pairs.append([p0,p1])
                query_pairs = xpair_query(pairs, schema, XQLIMIT)
                print(xrouter_emoticon,f"[bold magenta]XQuery[/bold magenta] for {'[bold yellow]pair[/bold yellow]' if len(XQPAIR)==1 else '[bold yellow]pairs[/bold yellow]'} {' '.join(XQPAIR)} ")
                results = run_query(HOST, query_pairs, PROJECTID, APIKEY)
                print(results)
            elif not XQPAIR and XQROUTER:
                query_routers = xfilter_query(XQROUTER, schema, XQLIMIT)
                print(xrouter_emoticon,f"[bold magenta]XQuery[/bold magenta] for {'[bold yellow]router[/bold yellow]' if len(XQROUTER)==1 else '[bold yellow]routers[/bold yellow]'} {' '.join(XQROUTER)} ")
                results = run_query(HOST, query_routers, PROJECTID, APIKEY)
                print(results)
            elif XQPAIR and XQROUTER:
                pairs = []
                for pair in XQPAIR:
                    if "/" not in pair or pair.count("/")!=1:
                        print(":x:",f"ignoring unknown format {pair}...")
                    else:
                        if XQPAIR.count(pair)==1:
                            p0 = pair.split("/")[0]
                            p1 = pair.split("/")[1]
                            pairs.append([p0,p1])
                query_pair_router = xpair_filter_query(pairs, XQROUTER, schema, XQLIMIT)
                print(xrouter_emoticon,f"[bold magenta]XQuery[/bold magenta] for {'[bold yellow]router[/bold yellow]' if len(XQROUTER)==1 else '[bold yellow]routers[/bold yellow]'} {' '.join(XQROUTER)} and {'pair' if len(XQPAIR)==1 else 'pairs'} {' '.join(XQPAIR)}")
                results = run_query(HOST, query_pair_router, PROJECTID, APIKEY)
                print(results)
            elif XQADDRESS:
                query_address = xaddress_query(XQADDRESS, schema, XQLIMIT)
                print(xrouter_emoticon,f"[bold magenta]XQuery[/bold magenta] for {'[bold yellow]address[/bold yellow]' if len(XQADDRESS)==1 else '[bold yellow]addresses[/bold yellow]'} {' '.join(XQADDRESS)}")
                results = run_query(HOST, query_address, PROJECTID, APIKEY)
                print(results)
            elif XQTX:
                query_tx = xtx_query(XQTX, schema)
                print(xrouter_emoticon,f"[bold magenta]XQuery[/bold magenta] for {'[bold yellow]TX[/bold yellow]' if len(XQTX)==1 else '[bold yellow]TXs[/bold yellow]'} {' '.join(XQTX)}")
                results = run_query(HOST, query_tx, PROJECTID, APIKEY)
                print(results)
            elif XQUERY:
                print(xrouter_emoticon,"[bold magenta]XQuery[/bold magenta] for [bold yellow]custom query[/bold yellow]")
                results = run_query(HOST, json.loads(XQUERY), PROJECTID, APIKEY)
                print(results)
            else:
                default = default_query(schema)
                print(xrouter_emoticon,"[bold magenta]XQuery[/bold magenta] for [bold yellow]last 20 entries[/bold yellow]")
                results = run_query(HOST, default, PROJECTID, APIKEY)
                print(results)
        elif XQHELP and PROJECTID:
            print(xrouter_emoticon,"[bold magenta]XQuery[/bold magenta] [bold yellow]help[/bold yellow]")
            results = run_help(HOST, PROJECTID)
            print(results)
        elif XQGRAPH and PROJECTID:
            print(xrouter_emoticon,"[bold magenta]XQuery[/bold magenta] [bold yellow]current graph[/bold yellow]")
            results = run_get_graph(HOST, PROJECTID)
            print(results)
        elif XQSCHEMA and PROJECTID:
            print(xrouter_emoticon,"[bold magenta]XQuery[/bold magenta] [bold yellow]schema[/bold yellow]")
            results = run_get_schema(HOST, PROJECTID)
            print(results)
        else:
            print(":x:","Missing [bold red]--projectid[/bold red] and/or [bold red]--apikey[/bold red]")
            parser.print_help()
    else:
        print(":x:","Missing [bold red]--host[/bold red]")
        parser.print_help()
