# xrouter-proxy-auto-deploy

# Requirements
- `Docker`
- `Docker-Compose`
- `Servicenode Private Key`
- `Port 80 must be opened on the host`

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
