# xrouter-proxy-auto-deploy for use with hydra

# Requirements
- `Docker`
- `Docker-Compose`
- `Servicenode Private Key`
- `Port 80 must be opened on the host`

# Supports external GETH host using gethexternal w/ deployscript (for use with archival node), otherwise a non geth-instance will be spun up
```
./deploy.sh gethexternal
```

# Recommended Usage
```
# Run deploy.sh
./deploy.sh

# Install Docker? [y/n] n
# Not installing Docker...
# Your Public IP Address: x.x.x.x
# Servicenode Name: example
# Servicenode Private Key: example
# Servicenode Address: example

# Please specify an user and password for the new servicenode
# RPC Username: example
# RPC Password: example
```

# Manual Usage
```
export PUBLIC_IP=""  # Update with your public ip address
export SN_NAME="servicenode01"  # Update with your snode name
export SN_KEY="servicenodeprivatekey"  # Update with your snode private key
export SN_ADDRESS="servicenodekeyaddress"  # Update with your snode address
export RPC_USER="user"
export RPC_PASSWORD="password"
docker-compose -f "docker-compose.yml" up -d --build
```

# Docker-Compose Environment Variables
* PUBLIC_IP - Your Public IP Address
* SN_NAME - Desired Servicenode Name
* SN_KEY - Servicenode Private Key 
* SN_ADDRESS - Servicenode Address
* RPC_USER - Desired RPC Username for all daemons
* RPC_PASSWORD - Desired RPC Password for all daemons

# Auto-Build Environment Variables
* MOUNT_DIR - Mount directory for daemons (defaults to /blockchain)
* DEPLOY_ETH - Whether GETH and ETH-Webserver should be deployed (defaults to true)

# bring down environment
```
docker-compose down
```

# Check geth accounts via console
```
function checkAllBalances() { var i =0; eth.accounts.forEach( function(e){ console.log("  eth.accounts["+i+"]: " +  e + " \tbalance: " + web3.fromWei(eth.getBalance(e), "ether") + " ether"); i++; })}; checkAllBalances();
```

# Create Project
```
Creates Hydra Project"
    Request Hydra Project, this creates project-id in db and gets ETH address for payment.
    Example: curl http://127.0.0.1/xrs/eth_passthrough \
                    -X POST \
                    -H "Content-Type: application/json" \
                    -d '{"jsonrpc":"2.0","method":"request_project","params": [],"id":1}'
                    
    results: "error":0,"result":{"api_key":"uiF_scQgopWWhgDFT7AMbM2Vf2b66xlfnVrJe6e1gUE","expiry_time":"2020-11-19 22:17:53 EST","payment_address":"0x0x0xxx","payment_amount_tier1":0.073597,"payment_amount_tier2":0.420557,"project_id":"85f1641d-f8ab-4acb-aa00-5d19601a9dd7"}}

```

# Request Data/Example call
```
curl http://127.0.0.1/xrs/eth_passthrough/<project_id> \
                    -X POST \
                    -H "Content-Type: application/json" \
                    -H "Api-Key: <API_Key>" \
                    -d '{"jsonrpc":"2.0","method":"net_version","params": [],"id":1}'
```

# Pricing
```
Set these values in USD:
      PAYMENT_AMOUNT_TIER1: 35
      PAYMENT_AMOUNT_TIER2: 200
https://github.com/blocknetdx/exrproxy-env/blob/master/docker-compose.yml#L83
```

# Checking stack

There are three python scripts to check API in auto_test directory:

- exr_methods.py - RPC calls to exr
- xrouter_methods.py - RCP calls to xrouter
- snode_methods.py - RPC calls to snode 

RPC methods are stored in json files. You are free to add/remove them. 

_More details in auto_test/README.md_

Examples: 

Retrieving the current block height of the longest chain for the specified blockchain.
_Make sure your xrouter config supports specified blockchain._ 
```bash 
python3 xrouter_methods.py LTC http://127.0.0.1 xrouter_methods.json 
----------------------------------------
Method xrGetBlockCount HTTP status code 200
1966098

python3 xrouter_methods.py BTC http://127.0.0.1 xrouter_methods.json 
----------------------------------------
Method xrGetBlockCount HTTP status code 200
2034177

python3 xrouter_methods.py BTC http://127.0.0.1 xrouter_methods.json 
----------------------------------------
Method xrGetBlockCount HTTP status code 200
2034177

python3 exr_methods.py project --api-key N8Zk0-hBRqD81dmBDEQP5qUpf9-XKz5eVPcstPkr8C0 --project-id 6228e1ed-1c78-40ca-9813-421d0fdfbfcf  http://127.0.0.1 exr_methods.json
---------------------------------------
Method eth_blockNumber HTTP status code 200
0xa2028a
---------------------------------------
Method eth_chainId HTTP status code 200
0x3
```
