#!/usr/bin/env python3
import yaml
import argparse
import os
#import logging
from jinja2 import Environment
from jinja2 import FileSystemLoader
from utils.loggerinit import *
from utils import autoconfig

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
    logging.info('processing custom:'.format(customlist))
    customlist[0]['mount_dir'] = os.environ.get("MOUNT_DIR", "/blockchain")

    for c in customlist:
        custom_template_fname = 'templates/{}'.format(c['j2template'])
        custom_template = J2_ENV.get_template(custom_template_fname)

        rendered_data = custom_template.render(c)
        rendered_filename = '{}{}-custom.yaml'.format(OUTPUT_PATH, c['name'])
        write_file(rendered_filename, rendered_data)


def processconfigs(datalist):
    XBRIDGE_CONF = "[Main]\nFullLog=true\nLogPath=\nExchangeTax=300\nExchangeWallets=BLOCK"

    for data in datalist:
        for daemon in data['daemons']:
            name = daemon['name']
            XBRIDGE_CONF += ",{}".format(name)

    XBRIDGE_CONF += "\n\n{}\n\n".format(autoconfig.generate_confs("BLOCK", 41412, 41414, os.environ.get("RPC_USER", "user"), os.environ.get("RPC_PASSWORD", "pass")))

    for data in datalist:
        for daemon in data['daemons']:
            name = daemon['name']
            p2pport = ''
            rpcport = ''
            username = os.environ.get("RPC_USER", "user")
            password = os.environ.get("RPC_PASSWORD", "pass")
            XBRIDGE_CONF += "{}\n\n".format(autoconfig.generate_confs(name, p2pport, rpcport, username, password))

    print(XBRIDGE_CONF)
    autoconfig.save_config(XBRIDGE_CONF, os.path.join('../scripts/config', 'xbridge.conf'))
            

if __name__ == "__main__":
    datalist = loadyaml(IMPORTYAML)
    if datalist == 'ERROR':
        logging.info('YAML LOAD FAILURE, check yaml format/file')
    else:
        processcustom(datalist)  # render dockercompose file
        # now we need xbridge files
        processconfigs(datalist)



