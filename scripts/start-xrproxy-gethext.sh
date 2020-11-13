#!/bin/bash

cat > /opt/uwsgi/conf/uwsgi.ini << EOL
[uwsgi]
processes = 4
threads = 4

buffer-size = 32768

set-ph = SERVICENODE_PRIVKEY=${SN_KEY}

set-ph = BLOCKNET_CHAIN=mainnet
set-ph = PLUGINS=eth_passthrough

set-ph = HANDLE_PAYMENTS=true
set-ph = HANDLE_PAYMENTS_ENFORCE=true
set-ph = HANDLE_PAYMENTS_RPC_INCLUDE_HEADERS=true
set-ph = HANDLE_PAYMENTS_RPC_HOSTIP=snode
set-ph = HANDLE_PAYMENTS_RPC_PORT=41414
set-ph = HANDLE_PAYMENTS_RPC_USER=${RPC_USER}
set-ph = HANDLE_PAYMENTS_RPC_PASS=${RPC_PASSWORD}
set-ph = HANDLE_PAYMENTS_RPC_VER=2.0

set-ph = RPC_BLOCK_HOSTIP=snode
set-ph = RPC_BLOCK_PORT=41414
set-ph = RPC_BLOCK_USER=${RPC_USER}
set-ph = RPC_BLOCK_PASS=${RPC_PASSWORD}
set-ph = RPC_BLOCK_VER=2.0

set-ph = URL_eth_accounts_HOSTIP=${GETH_HOST}
set-ph = URL_eth_accounts_PORT=8545

set-ph = URL_eth_blockNumber_HOSTIP=${GETH_HOST}
set-ph = URL_eth_blockNumber_PORT=8545

set-ph = URL_eth_call_HOSTIP=${GETH_HOST}
set-ph = URL_eth_call_PORT=8545

set-ph = URL_eth_chainId_HOSTIP=${GETH_HOST}
set-ph = URL_eth_chainId_PORT=8545

set-ph = URL_eth_estimateGas_HOSTIP=${GETH_HOST}
set-ph = URL_eth_estimateGas_PORT=8545

set-ph = URL_eth_gasPrice_HOSTIP=${GETH_HOST}
set-ph = URL_eth_gasPrice_PORT=8545

set-ph = URL_eth_getBalance_HOSTIP=${GETH_HOST}
set-ph = URL_eth_getBalance_PORT=8545

set-ph = URL_eth_getBlockByHash_HOSTIP=${GETH_HOST}
set-ph = URL_eth_getBlockByHash_PORT=8545

set-ph = URL_eth_getBlockByNumber_HOSTIP=${GETH_HOST}
set-ph = URL_eth_getBlockByNumber_PORT=8545

set-ph = URL_eth_getBlockTransactionCountByHash_HOSTIP=${GETH_HOST}
set-ph = URL_eth_getBlockTransactionCountByHash_PORT=8545

set-ph = URL_eth_getBlockTransactionCountByNumber_HOSTIP=${GETH_HOST}
set-ph = URL_eth_getBlockTransactionCountByNumber_PORT=8545

set-ph = URL_eth_getCode_HOSTIP=${GETH_HOST}
set-ph = URL_eth_getCode_PORT=8545

set-ph = URL_eth_getFilterChanges_HOSTIP=${GETH_HOST}
set-ph = URL_eth_getFilterChanges_PORT=8545

set-ph = URL_eth_getFilterLogs_HOSTIP=${GETH_HOST}
set-ph = URL_eth_getFilterLogs_PORT=8545

set-ph = URL_eth_getStorageAt_HOSTIP=${GETH_HOST}
set-ph = URL_eth_getStorageAt_PORT=8545

set-ph = URL_eth_getTransactionByBlockHashAndIndex_HOSTIP=${GETH_HOST}
set-ph = URL_eth_getTransactionByBlockHashAndIndex_PORT=8545

set-ph = URL_eth_getTransactionByBlockNumberAndIndex_HOSTIP=${GETH_HOST}
set-ph = URL_eth_getTransactionByBlockNumberAndIndex_PORT=8545

set-ph = URL_eth_getTransactionByHash_HOSTIP=${GETH_HOST}
set-ph = URL_eth_getTransactionByHash_PORT=8545

set-ph = URL_eth_getTransactionCount_HOSTIP=${GETH_HOST}
set-ph = URL_eth_getTransactionCount_PORT=8545

set-ph = URL_eth_getTransactionReceipt_HOSTIP=${GETH_HOST}
set-ph = URL_eth_getTransactionReceipt_PORT=8545

set-ph = URL_eth_getUncleByBlockHashAndIndex_HOSTIP=${GETH_HOST}
set-ph = URL_eth_getUncleByBlockHashAndIndex_PORT=8545

set-ph = URL_eth_getUncleByBlockNumberAndIndex_HOSTIP=${GETH_HOST}
set-ph = URL_eth_getUncleByBlockNumberAndIndex_PORT=8545

set-ph = URL_eth_getUncleCountByBlockHash_HOSTIP=${GETH_HOST}
set-ph = URL_eth_getUncleCountByBlockHash_PORT=8545

set-ph = URL_eth_getUncleCountByBlockNumber_HOSTIP=${GETH_HOST}
set-ph = URL_eth_getUncleCountByBlockNumber_PORT=8545

set-ph = URL_eth_getWork_HOSTIP=${GETH_HOST}
set-ph = URL_eth_getWork_PORT=8545

set-ph = URL_eth_hashrate_HOSTIP=${GETH_HOST}
set-ph = URL_eth_hashrate_PORT=8545

set-ph = URL_eth_mining_HOSTIP=${GETH_HOST}
set-ph = URL_eth_mining_PORT=8545

set-ph = URL_eth_newBlockFilter_HOSTIP=${GETH_HOST}
set-ph = URL_eth_newBlockFilter_PORT=8545

set-ph = URL_eth_newFilter_HOSTIP=${GETH_HOST}
set-ph = URL_eth_newFilter_PORT=8545

set-ph = URL_eth_newPendingTransactionFilter_HOSTIP=${GETH_HOST}
set-ph = URL_eth_newPendingTransactionFilter_PORT=8545

set-ph = URL_eth_protocolVersion_HOSTIP=${GETH_HOST}
set-ph = URL_eth_protocolVersion_PORT=8545

set-ph = URL_eth_sendRawTransaction_HOSTIP=${GETH_HOST}
set-ph = URL_eth_sendRawTransaction_PORT=8545

set-ph = URL_eth_submitWork_HOSTIP=${GETH_HOST}
set-ph = URL_eth_submitWork_PORT=8545

set-ph = URL_eth_syncing_HOSTIP=${GETH_HOST}
set-ph = URL_eth_syncing_PORT=8545

set-ph = URL_eth_uninstallFilter_HOSTIP=${GETH_HOST}
set-ph = URL_eth_uninstallFilter_PORT=8545

set-ph = URL_eth_unsubscribe_HOSTIP=${GETH_HOST}
set-ph = URL_eth_unsubscribe_PORT=8545

set-ph = URL_net_listening_HOSTIP=${GETH_HOST}
set-ph = URL_net_listening_PORT=8545

set-ph = URL_net_peerCount_HOSTIP=${GETH_HOST}
set-ph = URL_net_peerCount_PORT=8545

set-ph = URL_net_version_HOSTIP=${GETH_HOST}
set-ph = URL_net_version_PORT=8545

set-ph = URL_web3_clientVersion_HOSTIP=${GETH_HOST}
set-ph = URL_web3_clientVersion_PORT=8545

set-ph = URL_web3_sha3_HOSTIP=${GETH_HOST}
set-ph = URL_web3_sha3_PORT=8545

set-ph = URL_parity_allTransactionHashes_HOSTIP=${GETH_HOST}
set-ph = URL_parity_allTransactionHashes_PORT=8545

set-ph = URL_parity_allTransactions_HOSTIP=${GETH_HOST}
set-ph = URL_parity_allTransactions_PORT=8545

set-ph = URL_parity_unsubscribe_HOSTIP=${GETH_HOST}
set-ph = URL_parity_unsubscribe_PORT=8545
EOL

# ensure supervisord runs at pid1
exec supervisord -c /etc/supervisord.conf
