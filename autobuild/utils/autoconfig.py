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
from rich import print

def make_executable_files(path):
  files = os.listdir(path)
  for x in files:
    if x[-3::] == '.sh':
      make_executable(f'{path}/{x}')
  print(f'chmod +x {path}/*.sh')

def make_executable(path):
  mode = os.stat(path).st_mode
  mode |= (mode & 0o444) >> 2
  os.chmod(path, mode)

def write_text_file(filename, data):
  with open(filename,'w') as file:
    file.write(data)
    print(f"Wrote {filename}")

def write_yaml_file(filename, data):
  with open(filename, 'w') as file:
    yaml.dump(data, file, allow_unicode=True, sort_keys=False)
    print(f'Wrote {filename}')

def write_json_file(filename, data):
  with open(filename, 'w') as file:
    json.dump(data, file, sort_keys=False)
    print(f'Wrote {filename}')

def load_yaml_file(filename):
  print(f'Loading File: {filename}')
  try:
    with open(filename,'r') as fname:
      datalist = yaml.load(fname, Loader=yaml.FullLoader)
  except Exception as e:
    print('#ERROR loading yaml: {}'.format(e))
    return 'ERROR'
  return datalist

def load_text_file(filename):
  print(f'Loading File: {filename}')
  with open(f'{filename}','r') as file:
    data = file.read()
    return data

def load_json_file(filename):
  print(f'Loading File {filename}')
  with open(f'{filename}','r') as file:
    data = json.load(file)
    return data

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

def random_ip(subnet):
  #generate raandom ip from subnet
  all_ips = [str(x) for x in ipcalc.Network(subnet)]
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
