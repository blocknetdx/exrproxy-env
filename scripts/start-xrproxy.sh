#!/bin/bash

cat > /opt/uwsgi/conf/uwsgi.ini << EOL
[uwsgi]
processes = 4
threads = 4

buffer-size = 32768

set-ph = SERVICENODE_PRIVKEY=${SN_KEY}

set-ph = BLOCKNET_CHAIN=mainnet
set-ph = PLUGINS=eth_passthrough,xquery
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

set-ph = RPC_LTC_HOSTIP=LTC
set-ph = RPC_LTC_PORT=9332
set-ph = RPC_LTC_USER=${RPC_USER}
set-ph = RPC_LTC_PASS=${RPC_PASSWORD}
set-ph = RPC_LTC_VER=2.0

set-ph = RPC_DGB_HOSTIP=DGB
set-ph = RPC_DGB_PORT=14022
set-ph = RPC_DGB_USER=${RPC_USER}
set-ph = RPC_DGB_PASS=${RPC_PASSWORD}
set-ph = RPC_DGB_VER=2.0

set-ph = RPC_SYS_HOSTIP=SYS
set-ph = RPC_SYS_PORT=8370
set-ph = RPC_SYS_USER=${RPC_USER}
set-ph = RPC_SYS_PASS=${RPC_PASSWORD}
set-ph = RPC_SYS_VER=2.0

set-ph = RPC_PIVX_HOSTIP=PIVX
set-ph = RPC_PIVX_PORT=51473
set-ph = RPC_PIVX_USER=${RPC_USER}
set-ph = RPC_PIVX_PASS=${RPC_PASSWORD}
set-ph = RPC_PIVX_VER=2.0


set-ph = URL_XQUERY_HOSTIP=172.31.0.8
set-ph = URL_XQUERY_PORT=81

EOL
# ensure supervisord runs at pid1
exec supervisord -c /etc/supervisord.conf