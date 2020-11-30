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
    Example: curl http://127.0.0.1/xrs/eth_passthrough     -X POST     -H "Content-Type: application/json"     -d '{"jsonrpc":"2.0","method":"request_project","params": [],"id":1}'
    results: "error":0,"result":{"api_key":"uiF_scQgopWWhgDFT7AMbM2Vf2b66xlfnVrJe6e1gUE","expiry_time":"2020-11-19 22:17:53 EST","payment_address":"0x0x0xxx","payment_amount_tier1":0.073597,"payment_amount_tier2":0.420557,"project_id":"85f1641d-f8ab-4acb-aa00-5d19601a9dd7"}}

```
