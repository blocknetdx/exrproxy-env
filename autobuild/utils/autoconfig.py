#!/usr/bin/env python3

from jinja2 import Template
import json
import os, sys, os.path
import random
import string
import urllib.request
import argparse
import configparser

# MANIFEST_URL = 'https://raw.githubusercontent.com/blocknetdx/blockchain-configuration-files/master/manifest.json'

# from autobuild-generatetemplates branch (cleaned manifest)
MANIFEST_URL = 'https://raw.githubusercontent.com/blocknetdx/blockchain-configuration-files/autobuild-generatetemplates/manifest.json'
XBRIDGE_CONF_BASE_URL = 'https://raw.githubusercontent.com/blocknetdx/blockchain-configuration-files/master/xbridge-confs/'

walletconfj2_url = "https://raw.githubusercontent.com/blocknetdx/blockchain-configuration-files/autobuild-generatetemplates/autobuild/templates/wallet.conf.j2"
xbridgeconfj2_url = "https://raw.githubusercontent.com/blocknetdx/blockchain-configuration-files/autobuild-generatetemplates/autobuild/templates/xbridge.conf.j2"

def load_manifest():
  with urllib.request.urlopen(MANIFEST_URL) as response:
    data = json.loads(response.read())
    
  return data

manifest = load_manifest()

def load_template(template_url):
  # load_template - downloads from url provided and returns the data
  with urllib.request.urlopen(template_url) as response:
    data = response.read()
    result = data.decode('utf-8')
  return result


def chain_lookup(s):
  return "https://raw.githubusercontent.com/blocknetdx/blockchain-configuration-files/autobuild-generatetemplates/autobuild/configs/{}.base.j2".format(s.lower())


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

def Merge(dict1, dict2):
    res = {**dict1, **dict2}
    return res

def generate_confs(blockchain, p2pport, rpcport, username, password):
    if blockchain:
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
            return ""
        
        xtemplate = Template(xbridge_text)
        params = {}
        if p2pport:
            params['p2pPort'] = p2pport
        if rpcport:
            params['rpcPort'] = rpcport
        xresult = xtemplate.render(rpcusername=rpcuser, rpcpassword=rpcpass, **params)
        xbridge_json = json.loads(xresult)
        
        for sym in xbridge_json:
            if sym == 'BLOCK':
                continue
            
            xbridge_json[sym]['Ip'] = blockchain

        chain = next((c for c in manifest if c['ticker'] == blockchain), None)
        
        merged_dict = (Merge(chain,xbridge_json[chain['ticker']]))

        coin_title, p, this_coin_version = chain['ver_id'].partition('--')

        try:
            version_data = merged_dict['versions'][this_coin_version]
        except Exception as e:
            print('error, check manifest: {}'.format(chain['ticker']))
            print(merged_dict['versions'])
            raise Exception

        updated_dict = Merge(version_data,merged_dict) 
        # generate xbridge config
        xbridge_config = load_template(xbridgeconfj2_url)
        # f = open("xbridge.conf.j2", "r")
        # xbridge_config = f.read()
        xbridge_template = Template(xbridge_config)
        return xbridge_template.render(updated_dict)
