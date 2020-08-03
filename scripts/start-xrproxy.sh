#!/bin/bash

cat > /opt/uwsgi/conf/uwsgi.ini << EOL
[uwsgi]
processes = 4
threads = 4

buffer-size = 32768

set-ph = SERVICENODE_PRIVKEY=${SN_KEY}

set-ph = BLOCKNET_CHAIN=mainnet

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

set-ph = URL_eth_accounts_HOSTIP=eth_proxy
set-ph = URL_eth_accounts_PORT=9090

set-ph = URL_eth_blockNumber_HOSTIP=eth_proxy
set-ph = URL_eth_blockNumber_PORT=9090

set-ph = URL_eth_call_HOSTIP=eth_proxy
set-ph = URL_eth_call_PORT=9090

set-ph = URL_eth_chainId_HOSTIP=eth_proxy
set-ph = URL_eth_chainId_PORT=9090

set-ph = URL_eth_estimateGas_HOSTIP=eth_proxy
set-ph = URL_eth_estimateGas_PORT=9090

set-ph = URL_eth_gasPrice_HOSTIP=eth_proxy
set-ph = URL_eth_gasPrice_PORT=9090

set-ph = URL_eth_getBalance_HOSTIP=eth_proxy
set-ph = URL_eth_getBalance_PORT=9090

set-ph = URL_eth_getBlockByHash_HOSTIP=eth_proxy
set-ph = URL_eth_getBlockByHash_PORT=9090

set-ph = URL_eth_getBlockByNumber_HOSTIP=eth_proxy
set-ph = URL_eth_getBlockByNumber_PORT=9090

set-ph = URL_eth_getBlockTransactionCountByHash_HOSTIP=eth_proxy
set-ph = URL_eth_getBlockTransactionCountByHash_PORT=9090

set-ph = URL_eth_getBlockTransactionCountByNumber_HOSTIP=eth_proxy
set-ph = URL_eth_getBlockTransactionCountByNumber_PORT=9090

set-ph = URL_eth_getCode_HOSTIP=eth_proxy
set-ph = URL_eth_getCode_PORT=9090

set-ph = URL_eth_getFilterChanges_HOSTIP=eth_proxy
set-ph = URL_eth_getFilterChanges_PORT=9090

set-ph = URL_eth_getFilterLogs_HOSTIP=eth_proxy
set-ph = URL_eth_getFilterLogs_PORT=9090

set-ph = URL_eth_getStorageAt_HOSTIP=eth_proxy
set-ph = URL_eth_getStorageAt_PORT=9090

set-ph = URL_eth_getTransactionByBlockHashAndIndex_HOSTIP=eth_proxy
set-ph = URL_eth_getTransactionByBlockHashAndIndex_PORT=9090

set-ph = URL_eth_getTransactionByBlockNumberAndIndex_HOSTIP=eth_proxy
set-ph = URL_eth_getTransactionByBlockNumberAndIndex_PORT=9090

set-ph = URL_eth_getTransactionByHash_HOSTIP=eth_proxy
set-ph = URL_eth_getTransactionByHash_PORT=9090

set-ph = URL_eth_getTransactionCount_HOSTIP=eth_proxy
set-ph = URL_eth_getTransactionCount_PORT=9090

set-ph = URL_eth_getTransactionReceipt_HOSTIP=eth_proxy
set-ph = URL_eth_getTransactionReceipt_PORT=9090

set-ph = URL_eth_getUncleByBlockHashAndIndex_HOSTIP=eth_proxy
set-ph = URL_eth_getUncleByBlockHashAndIndex_PORT=9090

set-ph = URL_eth_getUncleByBlockNumberAndIndex_HOSTIP=eth_proxy
set-ph = URL_eth_getUncleByBlockNumberAndIndex_PORT=9090

set-ph = URL_eth_getUncleCountByBlockHash_HOSTIP=eth_proxy
set-ph = URL_eth_getUncleCountByBlockHash_PORT=9090

set-ph = URL_eth_getUncleCountByBlockNumber_HOSTIP=eth_proxy
set-ph = URL_eth_getUncleCountByBlockNumber_PORT=9090

set-ph = URL_eth_getWork_HOSTIP=eth_proxy
set-ph = URL_eth_getWork_PORT=9090

set-ph = URL_eth_hashrate_HOSTIP=eth_proxy
set-ph = URL_eth_hashrate_PORT=9090

set-ph = URL_eth_mining_HOSTIP=eth_proxy
set-ph = URL_eth_mining_PORT=9090

set-ph = URL_eth_newBlockFilter_HOSTIP=eth_proxy
set-ph = URL_eth_newBlockFilter_PORT=9090

set-ph = URL_eth_newFilter_HOSTIP=eth_proxy
set-ph = URL_eth_newFilter_PORT=9090

set-ph = URL_eth_newPendingTransactionFilter_HOSTIP=eth_proxy
set-ph = URL_eth_newPendingTransactionFilter_PORT=9090

set-ph = URL_eth_protocolVersion_HOSTIP=eth_proxy
set-ph = URL_eth_protocolVersion_PORT=9090

set-ph = URL_eth_sendRawTransaction_HOSTIP=eth_proxy
set-ph = URL_eth_sendRawTransaction_PORT=9090

set-ph = URL_eth_submitWork_HOSTIP=eth_proxy
set-ph = URL_eth_submitWork_PORT=9090

set-ph = URL_eth_syncing_HOSTIP=eth_proxy
set-ph = URL_eth_syncing_PORT=9090

set-ph = URL_eth_uninstallFilter_HOSTIP=eth_proxy
set-ph = URL_eth_uninstallFilter_PORT=9090

set-ph = URL_eth_unsubscribe_HOSTIP=eth_proxy
set-ph = URL_eth_unsubscribe_PORT=9090

set-ph = URL_net_listening_HOSTIP=eth_proxy
set-ph = URL_net_listening_PORT=9090

set-ph = URL_net_peerCount_HOSTIP=eth_proxy
set-ph = URL_net_peerCount_PORT=9090

set-ph = URL_net_version_HOSTIP=eth_proxy
set-ph = URL_net_version_PORT=9090

set-ph = URL_web3_clientVersion_HOSTIP=eth_proxy
set-ph = URL_web3_clientVersion_PORT=9090

set-ph = URL_web3_sha3_HOSTIP=eth_proxy
set-ph = URL_web3_sha3_PORT=9090

set-ph = URL_parity_allTransactionHashes_HOSTIP=eth_proxy
set-ph = URL_parity_allTransactionHashes_PORT=9090

set-ph = URL_parity_allTransactions_HOSTIP=eth_proxy
set-ph = URL_parity_allTransactions_PORT=9090

set-ph = URL_parity_unsubscribe_HOSTIP=eth_proxy
set-ph = URL_parity_unsubscribe_PORT=9090
EOL

supervisord -c /etc/supervisord.conf
