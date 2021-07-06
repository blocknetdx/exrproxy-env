###Auto tests
Scripts are used to test the basic functionality of SNODE. 

Libs: Unittest, requests, json

#### Before run script update rpcallowip=127.0.0.1 in start-snode.sh to allow requests.

unit_test.py - Scripts tests 4 RPC methods.
The methods are stored in the file template.json.

Exmaple
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

testmethods.py - Script sends requests to SNODE using RPC methods. 
The list of methods is located in the file xbridge_methods.json
It requires 4 arguments: HTTP socket, RPC username, RPC password, file with RPC methods.

Example:
```bash
$ python3 testmethods http://127.0.0.1:41414 user pass xbridge_methods.json


Method dxgetlocaltokens HTTP status code 200
['BLOCK', 'BTC', 'LTC'] 

Method dxgettokenbalances HTTP status code 200
{'Wallet': '0.000000', 'BLOCK': '0.000000', 'BTC': '0.000000', 'LTC': '0.000000'}



```



