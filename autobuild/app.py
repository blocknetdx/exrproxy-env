#!/usr/bin/env python3
import os
import json
import yaml
import argparse
#import logging
from jinja2 import Environment, FileSystemLoader, Template
from utils.loggerinit import *
from utils import autoconfig
from pprint import pprint as print

initialize_logger('')

J2_ENV = Environment(loader=FileSystemLoader(''),
                     trim_blocks=True)

parser = argparse.ArgumentParser()
parser.add_argument('--yaml', help='yaml filename to process', default='custom.yaml')
args = parser.parse_args()
IMPORTYAML = args.yaml
OUTPUT_PATH = './'

def loadyaml(yamlfilename):
    logging.info('Loading File: {}'.format(yamlfilename))
    try:
        with open(yamlfilename) as fname:
            datalist = yaml.load(fname, Loader=yaml.FullLoader)
    except Exception as e:
        logging.info('#ERROR loading yaml: {}'.format(e))
        return 'ERROR'
    return datalist


def write_file(filename, rendered_data):
    logging.info('Creating File: {}'.format(filename))
    with open(filename, "w") as fname:
        fname.write(rendered_data)
    return


def processcustom(customlist):
    # expects data in yaml, renders j2
    # logging.info('processing custom:'.format(customlist))
    logging.info('processing custom:')
    #customlist[0]['mount_dir'] = os.environ.get("MOUNT_DIR", "/blockchain")

    # volumes from custom.yaml
    for c in customlist:
        if 'volumes' in list(c):
            for i in range(len(c['volumes'])):
                name = c['volumes'][i]['name']
                if name == 'eth':
                    deploy_eth = os.environ.get("DEPLOY_ETH", "true")
                    customlist[0]['deploy_eth'] = True if str(deploy_eth).upper() == "TRUE" else False
                for j in list(c['volumes'][i]):
                    if j!='name':
                        mount_dir = f'{name}_{j}'
                        customlist[0][mount_dir] = os.environ.get(mount_dir.upper(),c['volumes'][i][j])


    for c in customlist:
        if 'volumes' not in list(c):
            for i in range(len(c['daemons'])):
                name = c['daemons'][i]['name']
                try:
                    logging.info(f'fetch template for {name} from raw.git')
                    xbridge_text = autoconfig.load_template(autoconfig.chain_lookup(name))
                    xtemplate = Template(xbridge_text)
                    xresult = xtemplate.render()
                    xbridge_json = json.loads(xresult)
                    c['daemons'][i]['p2pPort'] = xbridge_json[name]['p2pPort']
                    c['daemons'][i]['rpcPort'] = xbridge_json[name]['rpcPort']
                except Exception as e:
                    print("Config for currency {} not found".format(name))
                    return ""

            

            custom_template_fname = 'templates/{}'.format(c['j2template'])
            custom_template = J2_ENV.get_template(custom_template_fname)
            rendered_data = custom_template.render(c)
            rendered_filename = '{}{}-custom.yaml'.format(OUTPUT_PATH, c['name'])
            write_file(rendered_filename, rendered_data)


def processconfigs(datalist):
    XBRIDGE_CONF = "[Main]\nFullLog=true\nLogPath=\nExchangeTax=300\nExchangeWallets=BLOCK"

    # print(datalist)
    for data in datalist:
        if 'volumes' not in list(data):
            for daemon in data['daemons']:
                name = daemon['name']
                XBRIDGE_CONF += ",{}".format(name)

    XBRIDGE_CONF += "\n\n{}\n\n".format(autoconfig.generate_confs("BLOCK", 41412, 41414, os.environ.get("RPC_USER", "user"), os.environ.get("RPC_PASSWORD", "pass")))

    for data in datalist:
        if 'volumes' not in list(data):
            for daemon in data['daemons']:
                name = daemon['name']
                p2pport = ''
                rpcport = ''
                username = os.environ.get("RPC_USER", "user")
                password = os.environ.get("RPC_PASSWORD", "pass")
                XBRIDGE_CONF += "{}\n\n".format(autoconfig.generate_confs(name, p2pport, rpcport, username, password))

    autoconfig.save_config(XBRIDGE_CONF, os.path.join('../scripts/config', 'xbridge.conf'))
            

if __name__ == "__main__":
    datalist = loadyaml(IMPORTYAML)
    if datalist == 'ERROR':
        logging.info('YAML LOAD FAILURE, check yaml format/file')
    else:
        processcustom(datalist)  # render dockercompose file
        # now we need xbridge files
        processconfigs(datalist)



