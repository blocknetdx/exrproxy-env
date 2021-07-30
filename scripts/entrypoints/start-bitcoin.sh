#!/bin/bash

cat > /opt/blockchain/config/bitcoin.conf << EOL

rpcbind=0.0.0.0
rpcuser=${RPC_USER}
rpcpassword=${RPC_PASSWORD}
rpcallow=172.31.0.0/20

server=1
listen=1
rpcuser=
rpcpassword=
rpcallowip=0.0.0.0/0
port=8333
rpcport=8332
txindex=1


# Legacy addresses must be used
addresstype=legacy
changetype=legacy






EOL

# ensure docker runs daemon as pid1
exec $1