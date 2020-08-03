# xrouter-proxy-auto-deploy

# Requirements
- `Docker`
- `Docker-Compose`
- `Servicenode Private Key`

# Usage
```
export SN_NAME="servicenode01"
export SN_KEY="servicenodeprivatekey"
export SN_ADDRESS="servicenodekeyaddress"
export RPC_USER="user"
export RPC_PASSWORD="password"
docker-compose -f "docker-compose.yml" up -d --build
```
