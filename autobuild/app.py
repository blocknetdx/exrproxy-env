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
    #print(customlist)
    for c in customlist:
        custom_template_fname = 'templates/{}'.format(c['j2template'])
        print(custom_template_fname)
        custom_template = J2_ENV.get_template(custom_template_fname)

        rendered_data = custom_template.render(c)
        rendered_filename = '{}{}-custom.yaml'.format(OUTPUT_PATH, c['name'])
        write_file(rendered_filename, rendered_data)


def processconfigs(datalist):
    COIN_LIST = []
    for data in datalist:
        for daemon in data['daemons']:
            print(daemon['name'])
            COIN_LIST.append(daemon['name'])
            p2pport = ''
            rpcport = ''
            configname = ''
            username = '${RPC_USER}'
            password = '${RPC_PASSWORD}'
            chaindir = ''
            blocknetdir = ''
            blockdxdir = ''
            daemon = ''        
            autoconfig.generate_confs(COIN_LIST, p2pport, rpcport, configname, username, password,
                       chaindir, blocknetdir, blockdxdir, daemon)
            

if __name__ == "__main__":
    datalist = loadyaml(IMPORTYAML)
    if datalist == 'ERROR':
        logging.info('YAML LOAD FAILURE, check yaml format/file')
    else:
        processcustom(datalist)  # render dockercompose file
        # now we need xbridge files
        processconfigs(datalist)



