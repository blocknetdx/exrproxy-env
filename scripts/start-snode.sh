#!/bin/bash

cat > /opt/blockchain/config/blocknet.conf << EOL
datadir=/opt/blockchain/data

maxmempoolxbridge=128

port=41412
rpcport=41414

servicenode=1
daemon=0
listen=1
server=1
logtimestamps=1
logips=1
enableexchange=1
xrouter=1
rpcthreads=11

rpcuser=${RPC_USER}
rpcpassword=${RPC_PASSWORD}

rpcallowip=172.31.0.0/20
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
wallets=BLOCK,BTC,DASH,DGB,LTC,PIVX,SYS,LBC,MUE,PHR,RVN,GBX
#! plugins=eth_accounts,eth_blockNumber,eth_call,eth_chainId,eth_estimateGas,eth_gasPrice,eth_getBalance,eth_getBlockByHash,eth_getBlockByNumber,eth_getBlockTransactionCountByHash,eth_getBlockTransactionCountByNumber,eth_getCode,eth_getLogs,eth_getStorageAt,eth_getTransactionByBlockHashAndIndex,eth_getTransactionByBlockNumberAndIndex,eth_getTransactionByHash,eth_getTransactionCount,eth_getTransactionReceipt,eth_getUncleByBlockHashAndIndex,eth_getUncleByBlockNumberAndIndex,eth_getUncleCountByBlockHash,eth_getUncleCountByBlockNumber,eth_getWork,eth_hashrate,eth_mining,eth_protocolVersion,eth_sendRawTransaction,eth_submitWork,eth_syncing,eth_uninstallFilter,net_listening,net_peerCount,net_version,web3_clientVersion,web3_sha3,parity_allTransactionHashes,parity_allTransactions,eth_newBlockFilter,eth_newPendingTransactionFilter,eth_getFilterChanges,eth_getFilterLogs,eth_newFilter,eth_unsubscribe,parity_unsubscribe
plugins=projects,evm_passthrough,xquery
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
ExchangeWallets=BLOCK,BTC,DASH,DGB,LTC,PIVX,SYS,LBC,MUE,PHR,RVN,GBX

[BTC]
Title=Bitcoin
Address=
Ip=172.31.4.45
Port=8332
Username=${RPC_USER}
Password=${RPC_PASSWORD}
AddressPrefix=0
ScriptPrefix=5
SecretPrefix=128
COIN=100000000
MinimumAmount=0
TxVersion=2
DustAmount=0
CreateTxMethod=BTC
GetNewKeySupported=false
ImportWithNoScanSupported=false
MinTxFee=12000
BlockTime=600
FeePerByte=60
Confirmations=0

[DASH]
Title=Dash
Address=
Ip=172.31.2.13
Port=9998
Username=${RPC_USER}
Password=${RPC_PASSWORD}
AddressPrefix=76
ScriptPrefix=16
SecretPrefix=204
COIN=100000000
MinimumAmount=0
TxVersion=1
DustAmount=0
CreateTxMethod=BTC
GetNewKeySupported=false
ImportWithNoScanSupported=true
MinTxFee=2500
BlockTime=150
FeePerByte=5
Confirmations=0

[DGB]
Title=DigiByte
Address=
Ip=172.31.14.74
Port=14022
Username=${RPC_USER}
Password=${RPC_PASSWORD}
AddressPrefix=30
ScriptPrefix=63
SecretPrefix=128
COIN=100000000
MinimumAmount=0
TxVersion=1
DustAmount=0
CreateTxMethod=BTC
GetNewKeySupported=false
ImportWithNoScanSupported=true
MinTxFee=100000
BlockTime=15
FeePerByte=200
Confirmations=0

[LTC]
Title=Litecoin
Address=
Ip=172.31.6.239
Port=9332
Username=${RPC_USER}
Password=${RPC_PASSWORD}
AddressPrefix=48
ScriptPrefix=50
SecretPrefix=176
COIN=100000000
MinimumAmount=0
TxVersion=2
DustAmount=0
CreateTxMethod=BTC
GetNewKeySupported=true
ImportWithNoScanSupported=true
MinTxFee=5000
BlockTime=150
FeePerByte=10
Confirmations=0

[PIVX]
Title=PIVX
Address=
Ip=172.31.8.190
Port=51473
Username=${RPC_USER}
Password=${RPC_PASSWORD}
AddressPrefix=30
ScriptPrefix=13
SecretPrefix=212
COIN=100000000
MinimumAmount=0
TxVersion=1
DustAmount=0
CreateTxMethod=BTC
GetNewKeySupported=false
ImportWithNoScanSupported=true
MinTxFee=10000
BlockTime=60
FeePerByte=20
Confirmations=0

[SYS]
Title=Syscoin
Address=
Ip=172.31.3.40
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

[LBC]
Title=LBRYCredits
Address=
Ip=172.31.10.85
Port=9245
Username=${RPC_USER}
Password=${RPC_PASSWORD}
AddressPrefix=85
ScriptPrefix=122
SecretPrefix=28
COIN=100000000
MinimumAmount=0
TxVersion=1
DustAmount=0
CreateTxMethod=BTC
GetNewKeySupported=false
ImportWithNoScanSupported=true
MinTxFee=20000
BlockTime=150
FeePerByte=40
Confirmations=0

[MUE]
Title=MonetaryUnit
Address=
Ip=172.31.3.19
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
Ip=172.31.15.39
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

[RVN]
Title=Ravencoin
Address=
Ip=172.31.7.6
Port=8766
Username=${RPC_USER}
Password=${RPC_PASSWORD}
AddressPrefix=60
ScriptPrefix=122
SecretPrefix=128
COIN=100000000
MinimumAmount=0
TxVersion=1
DustAmount=0
CreateTxMethod=BTC
GetNewKeySupported=true
ImportWithNoScanSupported=true
MinTxFee=15000
BlockTime=60
FeePerByte=2500
Confirmations=0

[GBX]
Title=GoByte
Address=
Ip=172.31.1.120
Port=12454
Username=${RPC_USER}
Password=${RPC_PASSWORD}
AddressPrefix=38
ScriptPrefix=10
SecretPrefix=198
COIN=100000000
MinimumAmount=0
TxVersion=1
DustAmount=0
CreateTxMethod=BTC
GetNewKeySupported=true
ImportWithNoScanSupported=true
MinTxFee=2000
BlockTime=150
FeePerByte=4
Confirmations=0

[BLOCK]
Title=Blocknet
Address=
Ip=127.0.0.1
Port=41414
Username=${RPC_USER}
Password=${RPC_PASSWORD}
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


EOL

# ensure docker runs daemon as pid1
exec blocknetd