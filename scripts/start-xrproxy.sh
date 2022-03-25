#!/bin/bash

cat > /opt/uwsgi/conf/uwsgi.ini << EOL
[uwsgi]
processes = 4
threads = 4

buffer-size = 32768

set-ph = SERVICENODE_PRIVKEY=${SN_KEY}

set-ph = BLOCKNET_CHAIN=mainnet
set-ph = PLUGINS=projects,evm_passthrough,xquery
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

set-ph = RPC_BTC_HOSTIP=BTC
set-ph = RPC_BTC_PORT=8332
set-ph = RPC_BTC_USER=${RPC_USER}
set-ph = RPC_BTC_PASS=${RPC_PASSWORD}
set-ph = RPC_BTC_VER=2.0

set-ph = RPC_DASH_HOSTIP=DASH
set-ph = RPC_DASH_PORT=9998
set-ph = RPC_DASH_USER=${RPC_USER}
set-ph = RPC_DASH_PASS=${RPC_PASSWORD}
set-ph = RPC_DASH_VER=2.0

set-ph = RPC_DGB_HOSTIP=DGB
set-ph = RPC_DGB_PORT=14022
set-ph = RPC_DGB_USER=${RPC_USER}
set-ph = RPC_DGB_PASS=${RPC_PASSWORD}
set-ph = RPC_DGB_VER=2.0

set-ph = RPC_LTC_HOSTIP=LTC
set-ph = RPC_LTC_PORT=9332
set-ph = RPC_LTC_USER=${RPC_USER}
set-ph = RPC_LTC_PASS=${RPC_PASSWORD}
set-ph = RPC_LTC_VER=2.0

set-ph = RPC_PIVX_HOSTIP=PIVX
set-ph = RPC_PIVX_PORT=51473
set-ph = RPC_PIVX_USER=${RPC_USER}
set-ph = RPC_PIVX_PASS=${RPC_PASSWORD}
set-ph = RPC_PIVX_VER=2.0

set-ph = RPC_SYS_HOSTIP=SYS
set-ph = RPC_SYS_PORT=8370
set-ph = RPC_SYS_USER=${RPC_USER}
set-ph = RPC_SYS_PASS=${RPC_PASSWORD}
set-ph = RPC_SYS_VER=2.0

set-ph = RPC_LBC_HOSTIP=LBC
set-ph = RPC_LBC_PORT=9245
set-ph = RPC_LBC_USER=${RPC_USER}
set-ph = RPC_LBC_PASS=${RPC_PASSWORD}
set-ph = RPC_LBC_VER=2.0

set-ph = RPC_MUE_HOSTIP=MUE
set-ph = RPC_MUE_PORT=19688
set-ph = RPC_MUE_USER=${RPC_USER}
set-ph = RPC_MUE_PASS=${RPC_PASSWORD}
set-ph = RPC_MUE_VER=2.0

set-ph = RPC_PHR_HOSTIP=PHR
set-ph = RPC_PHR_PORT=11772
set-ph = RPC_PHR_USER=${RPC_USER}
set-ph = RPC_PHR_PASS=${RPC_PASSWORD}
set-ph = RPC_PHR_VER=2.0

set-ph = RPC_RVN_HOSTIP=RVN
set-ph = RPC_RVN_PORT=8766
set-ph = RPC_RVN_USER=${RPC_USER}
set-ph = RPC_RVN_PASS=${RPC_PASSWORD}
set-ph = RPC_RVN_VER=2.0

set-ph = RPC_GBX_HOSTIP=GBX
set-ph = RPC_GBX_PORT=12454
set-ph = RPC_GBX_USER=${RPC_USER}
set-ph = RPC_GBX_PASS=${RPC_PASSWORD}
set-ph = RPC_GBX_VER=2.0


set-ph = HYDRA=ETH,AVAX

set-ph = ETH_HOST_IP=172.31.9.99
set-ph = ETH_HOST_PORT=8545
set-ph = ETH_HOST_USER=
set-ph = ETH_HOST_PASS=
set-ph = ETH_HOST_DISALLOWED_METHODS=eth_accounts,db_putString,db_getString,db_putHex,db_getHex

set-ph = AVAX_HOST_IP=172.31.6.25
set-ph = AVAX_HOST_PORT=9650


set-ph = XQUERY_IP=172.31.1.114
set-ph = XQUERY_PORT=81

EOL
# ensure supervisord runs at pid1
exec supervisord -c /etc/supervisord.conf