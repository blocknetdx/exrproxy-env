#!/usr/bin/env python3
import os
import stat
import json
import re
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
parser.add_argument('--deploy_eth', help='Deploy ethereum stack', action='store_true')
parser.add_argument('--testnet', help='Use testnet', default=False)
parser.add_argument('--syncmode', help='sync mode', default='light')
parser.add_argument('--gethexternal', help='Use remote ethereum node', default=False)
parser.add_argument('--custom_manifest', help='URL to custom manifest files and configs', default=False)
args = parser.parse_args()
IMPORTYAML = args.yaml
DEPLOY_ETH = args.deploy_eth
GETHEXTERNAL = args.gethexternal
ETH_TESTNET = args.testnet
SYNCMODE = args.syncmode
CUSTOM_MANIFEST_URL = args.custom_manifest

if GETHEXTERNAL or ETH_TESTNET:
    DEPLOY_ETH = True
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
    daemonFiles = {}
    rpc_threads = 0
    if customlist[0]['custom_manifest']:
        manifest_config = autoconfig.load_template(re.sub(r'(^(?!.*/$).*)',r'\1/',customlist[0]['custom_manifest'])+'manifest-latest.json')
    else:
        manifest_config = autoconfig.load_template(autoconfig.manifest_content())
    manifest = json.loads(Template(manifest_config).render())
    for blockchain in manifest:
        daemonFiles[blockchain['ticker']] = blockchain['conf_name']

    for c in customlist:
        for i in range(len(c['daemons'])):
            name = c['daemons'][i]['name']
            #daemon configs
            if name.upper() not in ['SNODE', 'TNODE', 'TESTSNODE', 'ETH', 'XR_PROXY', 'AVAX']:
                try:
                    logging.info(f'fetch template for {name} from raw.git')
                    if customlist[0]['custom_manifest']:
                        xbridge_text = autoconfig.load_template(re.sub(r'(^(?!.*/$).*)',r'\1/',customlist[0]['custom_manifest'])+'autobuild/configs/{}.base.j2'.format(name.lower()))
                    else:
                        xbridge_text = autoconfig.load_template(autoconfig.chain_lookup(name))
                    xtemplate = Template(xbridge_text)
                    xresult = xtemplate.render()
                    xbridge_json = json.loads(xresult)

                    c['daemons'][i]['p2pPort'] = xbridge_json[name]['p2pPort']
                    c['daemons'][i]['rpcPort'] = xbridge_json[name]['rpcPort']
                    c['daemons'][i]['binFile'] = daemonFiles[name].split('.conf')[0]+'d'
                    c['daemons'][i]['configName'] = daemonFiles[name].split('.conf')[0]
                    tag = c['daemons'][i]['image'].split(':')[1]
                    if '-staging' in tag:
                        tag = tag.split('-staging')[0]
                    if tag != 'latest':
                        c['daemons'][i]['deprecatedrpc'] = xbridge_json[name]['versions'][tag]['deprecatedrpc']
                        c['daemons'][i]['legacy'] = xbridge_json[name]['versions'][tag]['legacy']
                    else:
                        version_list = list(xbridge_json[name]['versions'])
                        version_list.sort()
                        tag = version_list[-1]
                        c['daemons'][i]['deprecatedrpc'] = xbridge_json[name]['versions'][tag]['deprecatedrpc']
                        c['daemons'][i]['legacy'] = xbridge_json[name]['versions'][tag]['legacy']

                    while True:
                        custom_ip = autoconfig.random_ip()
                        if custom_ip not in used_ip.values():
                            c['daemons'][i]['ip'] = custom_ip
                            used_ip[name] = custom_ip
                            break
                    daemons_list.append(name.upper())
                    rpc_threads += 1
                except Exception as e:
                    print("Config for currency {} not found. The error is {}".format(name, e))
                    del c['daemons'][i]
            else:
                #others configs
                to_del_index.append(i)
                if name.upper() in ['XR_PROXY','AVAX', 'SNODE', 'TNODE', 'TESTSNODE']:
                    if name.upper() not in ['XR_PROXY', 'AVAX']:
                        customlist[0]['blocknet_image'] = c['daemons'][i]['image']
                        customlist[0]['blocknet_node'] = name.lower()
                    else:
                        customlist[0][f'{name.lower()}_image'] = c['daemons'][i]['image']
                    while True:
                        custom_ip = autoconfig.random_ip()
                        if custom_ip not in used_ip.values():
                            customlist[0][f'{name.lower()}_ip'] = custom_ip
                            used_ip[f'{name.lower()}_ip'] = custom_ip
                            break
                #deploy eth configs
                if name.upper() == 'ETH':
                    # deploy_eth = os.environ.get("DEPLOY_ETH", "true")
                    customlist[0][f'{name.lower()}_image'] = c['daemons'][i]['image']
                    # customlist[0]['deploy_eth'] = True if str(deploy_eth).upper() == "TRUE" else False
                    for k in ['PG','ETH','GETH']:
                        while True:
                            custom_ip = autoconfig.random_ip()
                            if custom_ip not in used_ip.values():
                                if k == 'GETH' and customlist[0]['gethexternal']:
                                    customlist[0][f'{k.lower()}_ip'] = customlist[0]['gethexternal']
                                    break
                                customlist[0][f'{k.lower()}_ip'] = custom_ip
                                used_ip[f'{k.lower()}_ip'] = custom_ip
                                break
                if name.upper() == 'AVAX':
                    customlist[0]['deploy_xquery'] = True
                    customlist[0]['plugins'].append('xquery')
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
                if set(tocomp_b).issubset(tocomp_a) == False:
                    #if daemons missing config add to to_del_index
                    logging.info(f'invalid config in YAML for {var["name"]}:\nmissing {list(set(tocomp_a).symmetric_difference(set(tocomp_b)))}')
                    to_del_index.append(index)
            elif var['name'].upper() in ['XR_PROXY', 'SNODE', 'TNODE', 'TESTSNODE', 'ETH', 'AVAX']:
                continue

        #delete fake daemons SNODE ETH XR_PROXY
        to_del_index.sort(reverse=True)
        for i in to_del_index:
            del c['daemons'][i]

        if rpc_threads > 8:
            c['rpcthreads'] = rpc_threads
        else:
            c['rpcthreads'] = 8

        custom_template_fname = 'templates/{}'.format(c['j2template'])
        custom_template = J2_ENV.get_template(custom_template_fname)
        rendered_data = custom_template.render(c)
        rendered_filename = '{}{}-custom.yaml'.format(OUTPUT_PATH, c['name'])
        write_file(rendered_filename, rendered_data)

        plugins = ''
        if len(customlist[0]['plugins']) >= 1:
            for i in customlist[0]['plugins']:
                plugins = plugins + i +','
            plugins = plugins[:-1]

        customlist[0]['xrouter_plugins'] = plugins

        return([c])


def processconfigs(datalist):
    # XBRIDGE_CONF = "[Main]\nFullLog=true\nLogPath=\nExchangeTax=300\nExchangeWallets=BLOCK"
    XBRIDGE_CONF = "[Main]\nFullLog=true\nLogPath=\nExchangeTax=300\nExchangeWallets=BLOCK,"

    custom_template_ec = J2_ENV.get_template('templates/entrypoint_config.j2')

    for data in datalist:
        for daemon in data['daemons']:
            name = daemon['name']
            if name.upper() not in ['TNODE', 'SNODE', 'TESTSNODE', 'ETH', 'XR_PROXY']:
                XBRIDGE_CONF += "{},".format(name)
                template_wc = Template(autoconfig.load_template(autoconfig.wallet_config())).render(daemon)
                rendered_data_ec = custom_template_ec.render({'walletConfig': template_wc,
                                                              'configName': daemon['configName']})
                config_name = '../scripts/entrypoints/start-{}.sh'.format(daemon['configName'])
                logging.info('Creating File: {}'.format(config_name))
                autoconfig.save_config(rendered_data_ec, config_name)
                st = os.stat(config_name)
                os.chmod(config_name, st.st_mode | stat.S_IEXEC)


    XBRIDGE_CONF = XBRIDGE_CONF[:-1]
    XBRIDGE_CONF += '\n\n'

    XR_TOKENS = ''
    for data in datalist:
        p2pport = ''
        rpcport = ''
        username = os.environ.get("RPC_USER", "${RPC_USER}")
        password = os.environ.get("RPC_PASSWORD", "${RPC_PASSWORD}")
        for daemon in data['daemons']:
            name = daemon['name']
            ip = daemon['ip']
            if name.upper() not in ['TNODE', 'SNODE', 'TESTSNODE', 'ETH', 'XR_PROXY']:
                XR_TOKENS += ','+name
                XBRIDGE_CONF += "{}\n\n".format(autoconfig.generate_confs(name, p2pport, rpcport, username, password, ip))
                logging.info('Add Xbridge: {}'.format(name))
        # ADD BLOCK settings
        XBRIDGE_CONF += "{}\n\n".format(autoconfig.generate_confs('block', p2pport, rpcport, username, password, '127.0.0.1'))

    autoconfig.save_config(XBRIDGE_CONF, os.path.join('../scripts/config', 'xbridge.conf'))
    custom_template_xr = J2_ENV.get_template('templates/xrouter.j2')
    XROUTER_CONF = custom_template_xr.render({'XR_TOKENS': XR_TOKENS, 'xrouter_plugins': datalist[0]['xrouter_plugins']})

    custom_template_snode = J2_ENV.get_template(f'templates/{datalist[0]["blocknet_node"]}.j2')
    datalist[0]['XROUTER_CONF'] = XROUTER_CONF
    datalist[0]['XBRIDGE_CONF'] = XBRIDGE_CONF
    rendered_data_snode = custom_template_snode.render(datalist[0])
    autoconfig.save_config(rendered_data_snode, f'../scripts/start-{datalist[0]["blocknet_node"]}.sh')

    custom_template_uw = J2_ENV.get_template('templates/xrproxy.j2')
    rendered_data_uw = custom_template_uw.render(datalist[0])
    autoconfig.save_config(rendered_data_uw, '../scripts/start-xrproxy.sh')

if __name__ == "__main__":
    datalist = loadyaml(IMPORTYAML)
    datalist[0]['plugins'] = []
    datalist[0]['deploy_eth'] = DEPLOY_ETH
    if datalist[0]['deploy_eth'] == True:
        datalist[0]['plugins'].append('eth_passthrough')
    datalist[0]['gethexternal'] = GETHEXTERNAL
    datalist[0]['eth_testnet'] = ETH_TESTNET
    datalist[0]['syncmode'] = SYNCMODE
    datalist[0]['custom_manifest'] = CUSTOM_MANIFEST_URL
    if datalist == 'ERROR':
        logging.info('YAML LOAD FAILURE, check yaml format/file')
    else:
        data_with_ips = processcustom(datalist)  # render dockercompose file
        # now we need xbridge files
        # processconfigs(datalist)
        processconfigs(data_with_ips)



