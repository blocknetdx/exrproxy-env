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
api_key : YR54ZEGcqyCvXcAn0Cj_eYFFzynrPDFpaREo2fa4lH4
expiry_time : 2021-07-12 00:04:26 EST
payment_address : 0x811D44BCBC689D50B90F3c391d7E0dB6A7BcDD69
payment_amount_tier1 : 0.016389
payment_amount_tier2 : 0.093652
project_id : 18e05f7a-4445-40de-9b6b-bb24b9a56e5c

```

In case of the getting project data 5 arguments

```bash
$ python3 exr_methods.py project --api-key N8Zk0-hBRqD81dmBDEQP5qUpf9-XKz5eVPcstPkr8C0 --project-id 6228e1ed-1c78-40ca-9813-421d0fdfbfcf  http://127.0.0.1 exr_methods.json
---------------------------------------
Method net_version HTTP status code 200
3
---------------------------------------
Method net_peerCount HTTP status code 200
0x1
---------------------------------------
Method eth_accounts HTTP status code 200
error : Unauthorized User Access
---------------------------------------
Method eth_blockNumber HTTP status code 200
0xa2028a
---------------------------------------
Method eth_chainId HTTP status code 200
0x3
---------------------------------------
Method eth_protocolVersion HTTP status code 200
jsonrpc : 2.0
id : exr
error : {'code': -32601, 'message': 'the method eth_protocolVersion does not exist/is not available'}
---------------------------------------
Method eth_getBalance HTTP status code 200
0x4563918244f40000
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
xquery_units.py - Script sends JSON-RPC requests to xquery container

The XQuery service is activated by plugin in Snode and Xrouter config. It is available through XRPoxy endpoints (/xrs/xquery)

example of request:
```bash 
curl http://127.0.0.1/xrs/xquery/ext/info
            -X POST                     
            -H "Content-Type: application/json"
            -d  '{"jsonrpc":"2.0", "id":1, "method" :"info.getBlockchainID",
                "params": { "alias":"X" }}'
```
```bash
python3 xquery_unit_test.py 
Chain X, blockchain id = 2oYMBNV4eNHyqk2fjjV5nVQLDbtmNJzq5s3qs3Lo6ftnC6FByM
Chain P, blockchain id = 11111111111111111111111111111111LpoYY
Chain C, blockchain id = 2q9e4r6Mu3U68nU1fYjgbR6JvwrRx36CohpAX5UQxse55x1Q5
.Chain X/tx,index 0, container id = qysTYUMCWdsR3MctzyfXiSvoSf6evbeFGRLLzA4j2BjNXTknh
Chain P/block,index 0, container id = 4AqeFPxtTW4B5D6oR8gRZTvRKnnqkUWiV6mUNZxjUMbQKYWpi
.
----------------------------------------------------------------------
Ran 2 tests in 0.071s

OK

```
