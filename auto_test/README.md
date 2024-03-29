###Auto tests
Scripts are used to test the basic functionality of SNODE, XROUTER and EXRproxy 

Libs: Unittest, requests, json

#### Before run script update rpcallowip=127.0.0.1 in start-snode.sh to allow requests.

unit_test.py - Scripts tests 4 RPC methods.
The methods are stored in the file template.json.
Before running unit_test.py, these 3 lines must be modified according to your environment:
    target = 'http://127.0.0.1:41414'
    user = 'user'
    password = 'pass'
If the snode is running in a docker container, the target IP needs to be changed from 127.0.0.1 to the ipv4_address of the container (found in docker-compose.yml).
user and password are the RPC user and RPC password of the snode.

Example
```bash
$ python3 unit_test.py


...F
======================================================================
FAIL: test_servicenodestatus (__main__.TestMethods)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/vr/blocknet/exrproxy-env/auto_test/unit_test.py", line 47, in test_servicenodestatus
    self.assertEqual(data, self.template['servicenodestatus'])
AssertionError: {'result': None, 'error': {'code': -32600, [110 chars]None} != {'status': 'running', 'services': ['BLOCK', 'BTC', 'LTC']}
+ {'services': ['BLOCK', 'BTC', 'LTC'], 'status': 'running'}
- {'error': {'code': -32600,
-            'message': 'No Service Node is running, check servicenode.conf or '
-                       'run the "servicenodesetup" command'},
-  'id': None,
-  'result': None}

----------------------------------------------------------------------
Ran 4 tests in 0.007s

FAILED (failures=1)


```

snode_methods.py - Script sends requests to SNODE using RPC methods. 
The list of methods is located in the file xbridge_methods.json
It requires 4 arguments: HTTP socket, RPC username, RPC password, file with RPC methods.

Example:
```bash
$ python3 snode_methods http://127.0.0.1:41414 user pass xbridge_methods.json
Note: If the snode is running in a docker container, the target IP needs to be changed from 127.0.0.1 to the ipv4_address of the container (found in docker-compose.yml).

Method dxgetlocaltokens HTTP status code 200
['BLOCK', 'BTC', 'LTC'] 

Method dxgettokenbalances HTTP status code 200
{'Wallet': '0.000000', 'BLOCK': '0.000000', 'BTC': '0.000000', 'LTC': '0.000000'}



```

exr_methods.py - Script sends JSON-RPC requests to EXRpoxy. 
The list of methods is located in the file exr_methods.json
It case of the creating a new project it takes 3 arguments:

- command (new_project or project)
- socket
- file with RPC methods

```bash
$ python3 exr_methods.py new_project http://127.0.0.1 exr_methods.json 
---------------------------------------
Method request_project HTTP status code 200
api_key : SgMbED-QDUjt6AFzW2SgANZeOJZhAwxpwdmm36XQpCU
expiry_time : 2022-02-04 22:32:29 EST
payment_amount_tier1_aablock : 1.795083
payment_amount_tier1_ablock : 0.625
payment_amount_tier1_eth : None
payment_amount_tier2_aablock : 359.016596
payment_amount_tier2_ablock : 125.0
payment_amount_tier2_eth : 0.067994
payment_avax_address : 0x977844F563590F4A4D90AEe07d9f0337BD18D3cc
payment_eth_address : 0x3713e2Db20fc393e9353A4b29c710D8E19411bCF
project_id : 99e02d11-c1a4-49ed-9ad0-4308a27dfcbe

```

In case of the getting project data 5 arguments

```bash
$ python3 exr_methods.py project --api-key N8Zk0-hBRqD81dmBDEQP5qUpf9-XKz5eVPcstPkr8C0 --project-id 6228e1ed-1c78-40ca-9813-421d0fdfbfcf  http://127.0.0.1 exr_methods.json
---------------------------------------
http://127.0.0.1/xrs/evm_passthrough/AVAX/f918cfa5-1ca7-4fb2-9d14-075e4b75d5fd/ext/bc/C/rpc
Method net_version HTTP status code 200
43114


---------------------------------------
http://127.0.0.1/xrs/evm_passthrough/AVAX/f918cfa5-1ca7-4fb2-9d14-075e4b75d5fd/ext/bc/C/rpc
Method net_peerCount HTTP status code 200
0x0


---------------------------------------
http://127.0.0.1/xrs/evm_passthrough/AVAX/f918cfa5-1ca7-4fb2-9d14-075e4b75d5fd/ext/bc/C/rpc
Method eth_accounts HTTP status code 200
error : Unauthorized User Access


---------------------------------------
http://127.0.0.1/xrs/evm_passthrough/AVAX/f918cfa5-1ca7-4fb2-9d14-075e4b75d5fd/ext/bc/C/rpc
Method eth_blockNumber HTTP status code 200
0xa00458


---------------------------------------
http://127.0.0.1/xrs/evm_passthrough/AVAX/f918cfa5-1ca7-4fb2-9d14-075e4b75d5fd/ext/bc/C/rpc
Method eth_chainId HTTP status code 200
0xa86a


---------------------------------------
http://127.0.0.1/xrs/evm_passthrough/AVAX/f918cfa5-1ca7-4fb2-9d14-075e4b75d5fd/ext/bc/C/rpc
Method eth_protocolVersion HTTP status code 200
jsonrpc : 2.0
id : exr
error : {'code': -32601, 'message': 'the method eth_protocolVersion does not exist/is not available'}


---------------------------------------
http://127.0.0.1/xrs/evm_passthrough/AVAX/f918cfa5-1ca7-4fb2-9d14-075e4b75d5fd/ext/bc/C/rpc
Method eth_getBalance HTTP status code 200
0x0


---------------------------------------
http://127.0.0.1/xrs/evm_passthrough/ETH/f918cfa5-1ca7-4fb2-9d14-075e4b75d5fd
Method net_version HTTP status code 200
1


---------------------------------------
http://127.0.0.1/xrs/evm_passthrough/ETH/f918cfa5-1ca7-4fb2-9d14-075e4b75d5fd
Method net_peerCount HTTP status code 200
0x4


---------------------------------------
http://127.0.0.1/xrs/evm_passthrough/ETH/f918cfa5-1ca7-4fb2-9d14-075e4b75d5fd
Method eth_accounts HTTP status code 200
error : Unauthorized User Access


---------------------------------------
http://127.0.0.1/xrs/evm_passthrough/ETH/f918cfa5-1ca7-4fb2-9d14-075e4b75d5fd
Method eth_blockNumber HTTP status code 200
0xd7c785


---------------------------------------
http://127.0.0.1/xrs/evm_passthrough/ETH/f918cfa5-1ca7-4fb2-9d14-075e4b75d5fd
Method eth_chainId HTTP status code 200
0x1


---------------------------------------
http://127.0.0.1/xrs/evm_passthrough/ETH/f918cfa5-1ca7-4fb2-9d14-075e4b75d5fd
Method eth_protocolVersion HTTP status code 200
jsonrpc : 2.0
id : exr
error : {'code': -32601, 'message': 'the method eth_protocolVersion does not exist/is not available'}


---------------------------------------
http://127.0.0.1/xrs/evm_passthrough/ETH/f918cfa5-1ca7-4fb2-9d14-075e4b75d5fd
Method eth_getBalance HTTP status code 200
0x0


```
Note: eth_accounts method is expected to fail with "Unauthorized User Access" That is as expected.

xrouter_methods.py - Script sends JSON-RPC requests to xrouter.

It takes 3 arguments

- token
- socket
- file with RPC methods
```bash
$ python3 xrouter_methods.py BLOCK http://127.0.0.1 xrouter_methods.json 
----------------------------------------
Method xrGetBlockCount HTTP status code 200
2058360

----------------------------------------
Method xrGetBlock HTTP status code 200
{'hash': '1769e76f5eae6adc7e9d560eacbd8f9860b952b87ff2148ee27127fa3265aa67',
 'confirmations': 42, 'strippedsize': 574, 'size': 610, 'weight': 2332, 'height': 2058319, 'version': 536870912,
  'versionHex': '20000000', 'merkleroot': 'ff8a97aaa6cec24a12b5e2dc659499b4abdbf1961076f5e18c6335a85d0f02ac', 
  'tx': ['bef2d6a2ab0de2ac2965e6a990c8a7602122dc9a9a0887870c7ca85e7367c895', 
  '329f014d9d2740a1420c38de17250f146421ce771056855c92eecdec6c338c93'],
   'time': 1626034093, 'mediantime': 1626033797, 'nonce': 1626034100, 'bits': '1b07cf70',
    'difficulty': 8390.839923728548, 'chainwork': '0000000000000000000000000000000000000000000000069fa98d424a9ed5ed', 
    'nTx': 2, 'previousblockhash': 'fdadd2aa4020b21a8906e9c061281681394db3810ef59b2b413ada42cae85670', 
    'nextblockhash': '7f5c8a57a845df626fa4e4795bb063969f4649f9bef0bf2f1b05c7ca92f462b5'}

---------------------------------------
Method xrGetTransaction HTTP status code 200
{'txid': 'bef2d6a2ab0de2ac2965e6a990c8a7602122dc9a9a0887870c7ca85e7367c895', 
'hash': '4570e372ca87dd137f1f2a4e3e2353fb91b18dd4982d16011156c555c879e2b3', 'version': 1, 'size': 148, 'vsize': 121,
 'weight': 484, 'locktime': 0, 'vin': [{'coinbase': '034f681f00', 'sequence': 4294967295}], 
 'vout': [{'value': 0.0, 'n': 0, 'scriptPubKey': {'asm': '', 'hex': '', 'type': 'nonstandard'}},
  {'value': 0.0, 'n': 1, 'scriptPubKey': {'asm': 'OP_RETURN aa21a9edf656f243d45aafd94a02e0051cad8067562583438c90f61ae3a03ce8222523d7',
   'hex': '6a24aa21a9edf656f243d45aafd94a02e0051cad8067562583438c90f61ae3a03ce8222523d7', 'type': 'nulldata'}}], 
   'hex': '010000000001010000000000000000000000000000000000000000000000000000000000000000ffffffff05034f681f00ffffffff020000000000000000000000000000000000266a24aa21a9edf656f243d45aafd94a02e0051cad8067562583438c90f61ae3a03ce8222523d70120000000000000000000000000000000000000000000000000000000000000000000000000', 
   'blockhash': '1769e76f5eae6adc7e9d560eacbd8f9860b952b87ff2148ee27127fa3265aa67', 'confirmations': 42, 'time': 1626034093, 'blocktime': 1626034093}
```
----------------------------

xquery_unit_test.py - XQuery tester. Checks for help and current graph

It takes 1 argument
-Project-ID of EXR project

```bash
python3 xquery_unit_test.py --projectid YOUR-PROJECT-ID
----------------------------------------
XQuery Help HTTP status code 200

Powered by
    https://blocknet.co
    https://xquery.io

List available endpoints
    http://<NODE-URL>/xrs/xquery/<PROJECT-ID>/help
    e.g. curl -X POST http://<NODE-URL>/xrs/xquery/<PROJECT-ID>/help 

Current Graph
    http://<NODE-URL>/xrs/xquery/<PROJECT-ID>/help/graph
    e.g. curl -X POST http://<NODE-URL>/xrs/xquery/<PROJECT-ID>/help/graph | jq

GraphQL data types
    http://<NODE-URL>/xrs/xquery/<PROJECT-ID>/help/schema
    e.g. curl -X POST http://<NODE-URL>/xrs/xquery/<PROJECT-ID>/help/schema

GraphQL endpoint
    http://<NODE-URL>/xrs/xquery/<PROJECT-ID>/indexer/
    e.g. See https://api.blocknet.co/#indexer-example



----------------------------------------
XQuery Current Graph HTTP status code 200

{"chains": [{"abi": "avax.json", "address": [{"address": "0xE54Ca86531e17Ef3616d22Ca28b0D458b6C89106", "name": "Pangolin_Router"}], "historical": [{"fromBlock": "6800000"}], "name": "AVAX", "query": [{"name": "Swap"}]}, {"abi": "eth.json", "address": [{"address": "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D", "name": "Uniswap_Router_v2"}, {"address": "0xe592427a0aece92de3edee1f18e0157c05861564", "name": "Uniswap_Router_v3"}], "historical": [{"fromBlock": "13600000"}], "name": "ETH", "query": [{"name": "Swap"}]}], "endpoint": "/indexer", "graph": "AVAX_ETH"}
```
----------------------------
