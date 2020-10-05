#!/bin/bash

cat > /opt/blockchain/config/blocknet.conf << EOL
datadir=/opt/blockchain/data

maxmempoolxbridge=128

port=41412
rpcport=41414

daemon=0
listen=1
server=1
logtimestamps=1
logips=1
servicenode=1
xrouter=1
rpcthreads=8

rpcuser=${RPC_USER}
rpcpassword=${RPC_PASSWORD}

rpcallowip=127.0.0.1
rpcbind=0.0.0.0
rpctimeout=30
rpcclienttimeout=30
EOL

cat > /opt/blockchain/data/servicenode.conf << EOL
# Service Node config
# Format: alias tier snodekey address
#   - alias can be any name, no spaces
#   - tier can be either SPV or OPEN
#   - snodekey must be a valid base58 encoded private key
#   - address must be a valid base58 encoded public key that contains the service node collateral
# SPV tier requires 5000 BLOCK collateral and an associated BLOCK address and can charge fees for services
# OPEN tier doesn't require any collateral, can't charge fees, and can only support XCloud plugins
# Example: dev OPEN 6BeBjrnd4DP5rEvUtxBQVu1DTPXUn6mCY5kPB2DWiy9CwEB2qh1
# Example: xrouter SPV 6B4VvHTn6BbHM3DRsf6M3Sk3jLbgzm1vp5jNe9ZYZocSyRDx69d Bj2w9gHtGp4FbVdR19tJZ9UHwWQhDXxGCM

${SN_NAME} SPV ${SN_KEY} ${SN_ADDRESS}
EOL

cat > /opt/blockchain/data/xrouter.conf << EOL
[Main]
#! host is a mandatory field, this tells the XRouter network how to find your node.
#! DNS and ip addresses are acceptable values.
#! host=mynode.example.com
#! host=208.67.222.222
host=${PUBLIC_IP}
wallets=BLOCK
plugins=eth_accounts,eth_blockNumber,eth_call,eth_chainId,eth_estimateGas,eth_gasPrice,eth_getBalance,eth_getBlockByHash,eth_getBlockByNumber,eth_getBlockTransactionCountByHash,eth_getBlockTransactionCountByNumber,eth_getCode,eth_getLogs,eth_getStorageAt,eth_getTransactionByBlockHashAndIndex,eth_getTransactionByBlockNumberAndIndex,eth_getTransactionByHash,eth_getTransactionCount,eth_getTransactionReceipt,eth_getUncleByBlockHashAndIndex,eth_getUncleByBlockNumberAndIndex,eth_getUncleCountByBlockHash,eth_getUncleCountByBlockNumber,eth_getWork,eth_hashrate,eth_mining,eth_protocolVersion,eth_sendRawTransaction,eth_submitWork,eth_syncing,eth_uninstallFilter,net_listening,net_peerCount,net_version,web3_clientVersion,web3_sha3,parity_allTransactionHashes,parity_allTransactions,eth_newBlockFilter,eth_newPendingTransactionFilter,eth_getFilterChanges,eth_getFilterLogs,eth_newFilter,eth_unsubscribe,parity_unsubscribe

#! port is the tcpip port on the host that accepts xrouter connections.
#! port will default to the default blockchain port (e.g. 41412), examples:
#! port=41412
#! port=80
#! port=8080
port=80

#! maxfee is the maximum fee (in BLOCK) you're willing to pay on a single xrouter call
#! 0 means you only want free calls
maxfee=0

#! consensus is the minimum number of nodes you want your xrouter calls to query (1 or more)
#! Paid calls will send a payment to each selected service node.
consensus=1

#! timeout is the maximum time in seconds you're willing to wait for an XRouter response
timeout=30
clientrequestlimit=50

[xrSendTransaction]
fee=0.0001
EOL

cat > /opt/blockchain/data/xbridge.conf << EOL
[Main]
ExchangeWallets=BLOCK
FullLog=true
LogPath=
ExchangeTax=300

[BLOCK]
Title=Blocknet
Ip=snode
Username=${RPC_USER}
Password=${RPC_PASSWORD}
Port=41414
AddressPrefix=26
ScriptPrefix=28
SecretPrefix=154
COIN=100000000
MinimumAmount=0
TxVersion=1
DustAmount=0
CreateTxMethod=BTC
GetNewKeySupported=true
ImportWithNoScanSupported=true
MinTxFee=10000
BlockTime=60
FeePerByte=20
Confirmations=0
Address=
TxWithTimeField=false
LockCoinsSupported=false
JSONVersion=
ContentType=
CashAddrPrefix=
EOL

blocknetd
