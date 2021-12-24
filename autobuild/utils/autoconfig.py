#!/usr/bin/env python3

from jinja2 import Template
import jinja2schema
import json
import os, sys, os.path
import random
import string
import urllib.request
import argparse
import configparser
import time
import ipcalc
import yaml

#MANIFEST_URL = 'https://raw.githubusercontent.com/blocknetdx/blockchain-configuration-files/master/manifest-latest.json'

#XBRIDGE_CONF_BASE_URL = 'https://raw.githubusercontent.com/blocknetdx/blockchain-configuration-files/master/xbridge-confs/'

#walletconfj2_url = "https://raw.githubusercontent.com/blocknetdx/blockchain-configuration-files/master/autobuild/templates/wallet.conf.j2"
#xbridgeconfj2_url = "https://raw.githubusercontent.com/blocknetdx/blockchain-configuration-files/master/autobuild/templates/xbridge.conf.j2"


def write_yaml_file(data):
  with open('xquery.yaml', 'w') as file:
    yaml.dump(data, file, allow_unicode=True)
    return('Wrote xquery.yaml')

def template_vars(template_path):
    #jinja2 all variables
    with open(template_path) as file:
        contents = file.read()
        contents = str(contents.split('#### XQUERY ####')[0])+str(contents.split('#### XQUERY ####')[-1])
        variables = jinja2schema.infer(contents)
        variables = jinja2schema.to_json_schema(variables)
        if 'chainstate_mount_dir' in variables['properties']['daemons']['items']['required']:
            variables['properties']['daemons']['items']['required'].remove('chainstate_mount_dir')
        #parse schema
        d = {}
        for req in variables['required']:
          d[req] = True
        d['daemons'] = {x:True for x in variables['properties']['daemons']['items']['required']}
        return(d)

def random_ip():
  #generate raandom ip from subnet
  all_ips = [str(x) for x in ipcalc.Network("172.31.0.0/20")]
  return(random.choice(all_ips))

def load_template(template_url):
  # load_template - downloads from url provided and returns the data
  while True:
    response = urllib.request.urlopen(template_url)
    if response.getcode() == 200:
      data = response.read()
      result = data.decode('utf-8')
      return result
    time.sleep(10)
    
def chain_lookup(BASE_URL, s):
	return BASE_URL + "/autobuild/configs/{}.base.j2".format(s.lower())

def manifest_content(BASE_URL):
	return BASE_URL + '/manifest-latest.json'

def wallet_config(BASE_URL):
	return BASE_URL + "/autobuild/templates/wallet.conf.j2"

def xbridge_config(BASE_URL):
	return BASE_URL + "/autobuild/templates/xbridge.conf.j2"

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

#generate confs IP dependent
def generate_confs(BASE_URL, blockchain, p2pport, rpcport, username, password, ip):
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
      xbridge_text = load_template(chain_lookup(BASE_URL, blockchain))
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
      # if sym == 'BLOCK':
      #   continue
      xbridge_json[sym]['Ip'] = ip

    # generate xbridge config
    #xbridge_config = load_template(xbridgeconfj2_url)
    xbridge_conf = load_template(xbridge_config(BASE_URL))
    xbridge_template = Template(xbridge_conf)
    
    chain = list(xbridge_json.keys())[0]
    xbridge_json[chain]['ticker'] = chain
    return xbridge_template.render(list(xbridge_json.values())[0])
