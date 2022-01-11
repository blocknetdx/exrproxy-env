#!/bin/bash

cat > /opt/blockchain/config/blocknet.conf << EOL
datadir=/opt/blockchain/data

maxmempoolxbridge=128

testnet=1
daemon=0
listen=1
server=1
logtimestamps=1
logips=1
servicenode=0
xrouter=1
rpcthreads=8

[test]
port=41474
rpcport=41419
addnode=54.158.97.146:41474
addnode=84.17.46.24:41474
addnode=207.180.193.54:41474
addnode=185.246.56.72:41474
addnode=5.189.189.252:41474
whitelist=54.158.97.146
whitelist=84.17.46.24
whitelist=207.180.193.54
whitelist=185.246.56.72
whitelist=5.189.189.252

rpcuser=${RPC_USER}
rpcpassword=${RPC_PASSWORD}

rpcallowip=172.31.0.0/20
rpcbind=0.0.0.0
rpctimeout=30
rpcclienttimeout=30
EOL


cat > /opt/blockchain/data/xrouter.conf << EOL
[Main]
#! host is a mandatory field, this tells the XRouter network how to find your node.
#! DNS and ip addresses are acceptable values.
#! host=mynode.example.com
#! host=208.67.222.222
host=${PUBLIC_IP}
wallets=TBLOCK,SYS,TBLOCK,MUE,PHR,UNO
#! plugins=eth_accounts,eth_blockNumber,eth_call,eth_chainId,eth_estimateGas,eth_gasPrice,eth_getBalance,eth_getBlockByHash,eth_getBlockByNumber,eth_getBlockTransactionCountByHash,eth_getBlockTransactionCountByNumber,eth_getCode,eth_getLogs,eth_getStorageAt,eth_getTransactionByBlockHashAndIndex,eth_getTransactionByBlockNumberAndIndex,eth_getTransactionByHash,eth_getTransactionCount,eth_getTransactionReceipt,eth_getUncleByBlockHashAndIndex,eth_getUncleByBlockNumberAndIndex,eth_getUncleCountByBlockHash,eth_getUncleCountByBlockNumber,eth_getWork,eth_hashrate,eth_mining,eth_protocolVersion,eth_sendRawTransaction,eth_submitWork,eth_syncing,eth_uninstallFilter,net_listening,net_peerCount,net_version,web3_clientVersion,web3_sha3,parity_allTransactionHashes,parity_allTransactions,eth_newBlockFilter,eth_newPendingTransactionFilter,eth_getFilterChanges,eth_getFilterLogs,eth_newFilter,eth_unsubscribe,parity_unsubscribe
plugins=
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
FullLog=true
LogPath=
ExchangeTax=300
ExchangeWallets=TBLOCK,SYS,TBLOCK,MUE,PHR,UNO

[SYS]
Title=Syscoin
Address=
Ip=172.31.11.37
Port=8370
Username=${RPC_USER}
Password=${RPC_PASSWORD}
AddressPrefix=63
ScriptPrefix=5
SecretPrefix=128
COIN=100000000
MinimumAmount=0
TxVersion=1
DustAmount=0
CreateTxMethod=BTC
GetNewKeySupported=true
ImportWithNoScanSupported=true
MinTxFee=20000
BlockTime=150
FeePerByte=40
Confirmations=0

[TBLOCK]
Title=Blocknet Testnet
Address=
Ip=172.31.6.189
Port=41419
Username=${RPC_USER}
Password=${RPC_PASSWORD}
AddressPrefix=139
ScriptPrefix=19
SecretPrefix=239
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

[MUE]
Title=MonetaryUnit
Address=
Ip=172.31.0.122
Port=19688
Username=${RPC_USER}
Password=${RPC_PASSWORD}
AddressPrefix=16
ScriptPrefix=76
SecretPrefix=126
COIN=100000000
MinimumAmount=0
TxVersion=1
DustAmount=0
CreateTxMethod=BTC
GetNewKeySupported=false
ImportWithNoScanSupported=true
MinTxFee=10000
BlockTime=40
FeePerByte=20
Confirmations=0

[PHR]
Title=Phore
Address=
Ip=172.31.4.64
Port=11772
Username=${RPC_USER}
Password=${RPC_PASSWORD}
AddressPrefix=55
ScriptPrefix=13
SecretPrefix=212
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

[UNO]
Title=Unobtanium
Address=
Ip=172.31.0.112
Port=65535
Username=${RPC_USER}
Password=${RPC_PASSWORD}
AddressPrefix=130
ScriptPrefix=30
SecretPrefix=224
COIN=100000000
MinimumAmount=0
TxVersion=1
DustAmount=0
CreateTxMethod=BTC
GetNewKeySupported=true
ImportWithNoScanSupported=true
MinTxFee=1000
BlockTime=180
FeePerByte=3
Confirmations=0

[TBLOCK]
Title=Blocknet Testnet
Address=
Ip=127.0.0.1
Port=41419
Username=${RPC_USER}
Password=${RPC_PASSWORD}
AddressPrefix=139
ScriptPrefix=19
SecretPrefix=239
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


EOL

# ensure docker runs daemon as pid1
exec blocknetd