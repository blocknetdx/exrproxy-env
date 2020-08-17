#!/usr/bin/env python3

from jinja2 import Template
import json
import os, sys, os.path
import random
import string
import urllib.request
import argparse
import configparser

#
MANIFEST_URL = 'https://raw.githubusercontent.com/blocknetdx/blockchain-configuration-files/master/manifest.json'
WALLET_CONF_BASE_URL = 'https://raw.githubusercontent.com/blocknetdx/blockchain-configuration-files/master/wallet-confs/'
XBRIDGE_CONF_BASE_URL = 'https://raw.githubusercontent.com/blocknetdx/blockchain-configuration-files/master/xbridge-confs/'

walletconfj2_url = "https://raw.githubusercontent.com/BlocknetDX/blocknet-docs/master/json-config-templates/wallet.conf.j2"
xbridgeconfj2_url = "https://raw.githubusercontent.com/BlocknetDX/blocknet-docs/master/json-config-templates/xbridge.conf.j2"


def load_template(template_url):
  # load_template - downloads from url provided and returns the data
  with urllib.request.urlopen(template_url) as response:
    data = response.read()
    result = data.decode('utf-8')
  return result


def chain_lookup(s):
  return "https://raw.githubusercontent.com/BlocknetDX/blocknet-docs/master/json-config-templates/{}.json.j2".format(s.lower())


def random_gen(size=32, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
  return ''.join(random.choice(chars) for x in range(size))


def save_config(configData, confFile):
  with open(confFile, 'w') as outfile:
    #out.write(data, outfile)
    outfile.write(configData)
  return


def load_url(load_url):
  # load_template - downloads from url provided and returns the data
  with urllib.request.urlopen(load_url) as response:
    data = response.read()
    result = data.decode('utf-8')
  return result


def parse_config(config_string):
    return config_string.splitlines()


def generate_confs(blockchain, p2pport, rpcport, configname, username, password, chaindir, blocknetdir, blockdxdir, daemon):
    if blockchain:
        if len(blockchain) > 1:
            if p2pport:
                print("Warning: parameter --p2pport ignored because multiple blockchains were selected.")
            if rpcport:
                print("Warning: parameter --rpcport ignored because multiple blockchains were selected.")
            if chaindir:
                print("Warning: parameter --chaindir ignored because multiple blockchains were selected.")
            if configname:
                print("Warning: parameter --configname ignored because multiple blockchains were selected.")
            p2pport = rpcport = configname = chaindir = None
        if chaindir is None:
            chaindir = '.'
        if blocknetdir is None:
            blocknetdir = '.'
        if blockdxdir is None:
            blockdxdir = '.'
        for blockchain in blockchain:
            if username is None:
                rpcuser = random_gen()
            else:
                rpcuser = username
            if password is None:
                rpcpass = random_gen()
            else:
                rpcpass = password
            # find the URL for the chain
            try:
                xbridge_text = load_template(chain_lookup(blockchain))
            except urllib.error.HTTPError as e:
                print("Config for currency {} not found".format(blockchain))
                continue
            xbridge_json = json.loads(xbridge_text)
            xtemplate = Template(xbridge_text)
            params = {}
            if p2pport:
                params['p2pPort'] = p2pport
            if rpcport:
                params['rpcPort'] = rpcport
            xresult = xtemplate.render(rpcusername=rpcuser, rpcpassword=rpcpass, **params)
            xbridge_json = json.loads(xresult)

            confFile = list(xbridge_json.values())[0]['Title'].lower()
            if configname:
                confFile = args.configname.lower()

            # generate wallet config
            for x in xbridge_json: p2pport = (xbridge_json[x]['p2pPort'])
            for x in xbridge_json: rpcport = (xbridge_json[x]['rpcPort'])
            res_conf = load_template(walletconfj2_url)
            template = Template(res_conf)
            result = template.render(rpcusername=rpcuser, rpcpassword=rpcpass, p2pPort=p2pport, rpcPort=rpcport)
            if daemon:
                result += "\ndaemon=1"
            save_config(result, os.path.join(chaindir, '%s.conf' % confFile))

            # generate xbridge config
            xbridge_config = load_template(xbridgeconfj2_url)
            # f = open("xbridge.conf.j2", "r")
            # xbridge_config = f.read()
            xbridge_template = Template(xbridge_config)
            xbridge_result = xbridge_template.render(blockchain=blockchain, val=list(xbridge_json.values())[0])
            save_config(xbridge_result, os.path.join(blocknetdir, confFile + '-xbridge.conf'))
