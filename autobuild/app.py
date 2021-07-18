#!/usr/bin/env python3
import os
import json
import yaml
import argparse
import logging
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
    print(customlist)
    used_ip = {}
    to_del_index = []
    daemons_list = []
    for c in customlist:
        for i in range(len(c['daemons'])):
            name = c['daemons'][i]['name']
            #daemon configs
            if name.upper() not in ['SNODE','ETH','XR_PROXY']:
                try:
                    logging.info(f'fetch template for {name} from raw.git')
                    xbridge_text = autoconfig.load_template(autoconfig.chain_lookup(name))
                    xtemplate = Template(xbridge_text)
                    xresult = xtemplate.render()
                    xbridge_json = json.loads(xresult)
                    c['daemons'][i]['p2pPort'] = xbridge_json[name]['p2pPort']
                    c['daemons'][i]['rpcPort'] = xbridge_json[name]['rpcPort']
                    while True:
                        custom_ip = autoconfig.random_ip()
                        if custom_ip not in used_ip.values():
                            c['daemons'][i]['ip'] = custom_ip
                            used_ip[name]=custom_ip
                            break
                    daemons_list.append(name.upper())
                except Exception as e:
                    print("Config for currency {} not found".format(name))
                    return ""
            else:
                #others configs
                to_del_index.append(i)
                if name.upper() in ['XR_PROXY','SNODE']:
                    customlist[0][f'{name.lower()}_image'] = c['daemons'][i]['image']
                    while True:
                        custom_ip = autoconfig.random_ip()
                        if custom_ip not in used_ip.values():
                            customlist[0][f'{name.lower()}_ip'] = custom_ip
                            used_ip[f'{name.lower()}_ip'] = custom_ip
                            break
                #deploy eth configs
                if name.upper() == 'ETH':
                    deploy_eth = os.environ.get("DEPLOY_ETH", "true")
                    customlist[0][f'{name.lower()}_image'] = c['daemons'][i]['image']
                    customlist[0]['deploy_eth'] = True if str(deploy_eth).upper() == "TRUE" else False
                    for k in ['PG','ETH','GETH']:
                        while True:
                            custom_ip = autoconfig.random_ip()
                            if custom_ip not in used_ip.values():
                                customlist[0][f'{k.lower()}_ip'] = custom_ip
                                used_ip[f'{k.lower()}_ip'] = custom_ip
                                break
                #volumes paths configs
                for j in list(c['daemons'][i]):
                    if j not in ['name','image']:
                        mount_dir = f'{name.lower()}_{j}'
                        customlist[0][mount_dir] = os.environ.get(mount_dir.upper(),c['daemons'][i][j])
        
        #check for missed configs
        #loading template vars
        template_vars = autoconfig.template_vars('templates/{}'.format(c['j2template']))

        for index, var in enumerate(c['daemons']):
            #check if fake daemon or not (SNODE ETH XR_PROXY)
            if var['name'] in daemons_list:
                #compare daemons with template
                tocomp_a = list(var)
                tocomp_b = list(template_vars['daemons'])
                tocomp_a.sort()
                tocomp_b.sort()
                if tocomp_a != tocomp_b:
                    #if daemons missing config add to to_del_index
                    logging.info(f'invalid config in YAML for {var["name"]}:\nmissing {list(set(tocomp_a).symmetric_difference(set(tocomp_b)))}')
                    to_del_index.append(index)
            elif var['name'].upper() in ['XR_PROXY','SNODE','ETH']:
                continue

        #delete fake daemons SNODE ETH XR_PROXY
        to_del_index.sort(reverse=True)
        for i in to_del_index:
            del c['daemons'][i]

        custom_template_fname = 'templates/{}'.format(c['j2template'])
        custom_template = J2_ENV.get_template(custom_template_fname)
        rendered_data = custom_template.render(c)
        rendered_filename = '{}{}-custom.yaml'.format(OUTPUT_PATH, c['name'])
        write_file(rendered_filename, rendered_data)


        return([c])


def processconfigs(datalist):
    # XBRIDGE_CONF = "[Main]\nFullLog=true\nLogPath=\nExchangeTax=300\nExchangeWallets=BLOCK"
    XBRIDGE_CONF = "[Main]\nFullLog=true\nLogPath=\nExchangeTax=300\nExchangeWallets="

    # print(datalist)
    for data in datalist:
        for daemon in data['daemons']:
            name = daemon['name']
            if name.upper() not in ['SNODE','ETH','XR_PROXY']:
                XBRIDGE_CONF += "{},".format(name)
    XBRIDGE_CONF = XBRIDGE_CONF[:-1]
    XBRIDGE_CONF += '\n\n'

    # XBRIDGE_CONF += "\n\n{}\n\n".format(autoconfig.generate_confs("BLOCK", 41412, 41414, os.environ.get("RPC_USER", "user"), os.environ.get("RPC_PASSWORD", "pass")))
    XR_TOKENS = ''
    for data in datalist:
        for daemon in data['daemons']:
            name = daemon['name']
            ip = daemon['ip']
            if name.upper() not in ['SNODE','ETH','XR_PROXY']:
                XR_TOKENS += ','+name
                p2pport = ''
                rpcport = ''
                username = os.environ.get("RPC_USER", "${RPC_USER}")
                password = os.environ.get("RPC_PASSWORD", "${RPC_PASSWORD}")
                XBRIDGE_CONF += "{}\n\n".format(autoconfig.generate_confs(name, p2pport, rpcport, username, password, ip))

    autoconfig.save_config(XBRIDGE_CONF, os.path.join('../scripts/config', 'xbridge.conf'))

    custom_template_xr = J2_ENV.get_template('templates/xrouter.j2')
    XROUTER_CONF = custom_template_xr.render({'XR_TOKENS': XR_TOKENS})

    custom_template_snode = J2_ENV.get_template('templates/snode.j2')
    rendered_data_snode = custom_template_snode.render({'XROUTER_CONF': XROUTER_CONF,
                                                        'XBRIDGE_CONF': XBRIDGE_CONF})

    autoconfig.save_config(rendered_data_snode, '../scripts/start-snode.sh')

    custom_template_uw = J2_ENV.get_template('templates/xrproxy.j2')
    rendered_data_uw = custom_template_uw.render(datalist[0])
    autoconfig.save_config(rendered_data_uw, '../scripts/start-xrproxy.sh')

if __name__ == "__main__":
    datalist = loadyaml(IMPORTYAML)
    if datalist == 'ERROR':
        logging.info('YAML LOAD FAILURE, check yaml format/file')
    else:
        # print(datalist)
        data_with_ips = processcustom(datalist)  # render dockercompose file
        # now we need xbridge files
        # processconfigs(datalist)
        processconfigs(data_with_ips)



