#!/usr/bin/env python3
import os
import stat
import json
import re
import ipaddress
from jinja2 import Environment, FileSystemLoader, Template, BaseLoader
from autobuild.utils.autoconfig import *
import autobuild.utils.autoconfig as autoconfig
from autobuild.utils.xquery import xq_template
from autobuild.utils.utxo import utxo_template
from icecream import ic, install
from rich import print

ic.configureOutput(includeContext=True)   # show context
install()                                 # make available to imported modules

J2_ENV = Environment(loader=FileSystemLoader(''),
					 trim_blocks=True)

J2_ENV2 = Environment(loader=BaseLoader(),
					 trim_blocks=True)


OUTPUT_PATH = './'
IPS_CACHE = '.cache_ip'
UTXO_PLUGIN_METHODS = ['getutxos','getrawtransaction','getrawmempool','getblockcount','sendrawtransaction','gettransaction','getblock','getblockhash','heights','fees','getbalance','gethistory','ping']

def processcustom(customlist, SUBNET, BRANCHPATH):
	if IPS_CACHE not in os.listdir(os.getcwd()):
		write_text_file(IPS_CACHE,json.dumps({'ip':{}}, indent=4, sort_keys=False))
	used_ip = json.loads(load_text_file(os.getcwd()+'/'+IPS_CACHE))

	print('Processing custom input...')
	to_del_index = []
	daemons_list = []
	configFiles = {}
	binFiles = {}
	rpc_threads = 0
	manifest_config = autoconfig.load_template(autoconfig.manifest_content(BRANCHPATH))
	manifest = json.loads(Template(manifest_config).render())
	for blockchain in manifest:
		configFiles[blockchain['ticker']] = blockchain['conf_name']
		if 'daemon_stem' in blockchain: # eg: SCC, XVG have non-standard daemon names
			binFiles[blockchain['ticker']] = blockchain['daemon_stem'] + 'd'
		else:
			binFiles[blockchain['ticker']] = blockchain['conf_name'].split('.conf')[0] + 'd'

	customlist[0]['deploy_nevm'] = False
	for c in customlist:
		for i in range(len(c['daemons'])):
			name = c['daemons'][i]['name']
			type = c['daemons'][i]['type']
			#daemon configs
			if type in ['chain', 'hybrid']:
				try:
					print(f'fetch template for {name} from raw.git')
					xbridge_text = autoconfig.load_template(autoconfig.chain_lookup(BRANCHPATH, name))
					xtemplate = Template(xbridge_text)
					xresult = xtemplate.render()
					xbridge_json = json.loads(xresult)
					c['daemons'][i]['p2pPort'] = xbridge_json[name]['p2pPort']
					c['daemons'][i]['rpcPort'] = xbridge_json[name]['rpcPort']
					c['daemons'][i]['binFile'] = binFiles[name]
					c['daemons'][i]['configName'] = configFiles[name].split('.conf')[0]
					tag = c['daemons'][i]['image'].split(':')[1]
					if '-staging' in tag:
						tag = tag.split('-staging')[0]
					if tag != 'latest':
						c['daemons'][i]['deprecatedrpc'] = xbridge_json[name]['versions'][tag]['deprecatedrpc']
						c['daemons'][i]['legacy'] = xbridge_json[name]['versions'][tag]['legacy']
						if 'rpcserialversion' in xbridge_json[name]['versions'][tag]:
							c['daemons'][i]['rpcserialversion'] = xbridge_json[name]['versions'][tag]['rpcserialversion']						
						if 'testnet' in xbridge_json[name]['versions'][tag]: 
							c['daemons'][i]['testnet'] = xbridge_json[name]['versions'][tag]['testnet']
						else:
							c['daemons'][i]['testnet'] = False
					else:
						version_list = list(xbridge_json[name]['versions'])
						version_list.sort()
						tag = version_list[-1]
						c['daemons'][i]['deprecatedrpc'] = xbridge_json[name]['versions'][tag]['deprecatedrpc']
						c['daemons'][i]['legacy'] = xbridge_json[name]['versions'][tag]['legacy']
						if 'rpcserialversion' in xbridge_json[name]['versions'][tag]:
							c['daemons'][i]['rpcserialversion'] = xbridge_json[name]['versions'][tag]['rpcserialversion']
						if 'testnet' in xbridge_json[name]['versions'][tag]: 
							c['daemons'][i]['testnet'] = xbridge_json[name]['versions'][tag]['testnet']
						else:
							c['daemons'][i]['testnet'] = False
					if name in used_ip['ip'].keys():
						c['daemons'][i]['ip'] = used_ip['ip'][name]
					else:
						while True:
							custom_ip = autoconfig.random_ip(SUBNET)
							if custom_ip not in used_ip['ip'].values():
								c['daemons'][i]['ip'] = custom_ip
								used_ip['ip'][name] = custom_ip
								break
					if name == 'SYS':
						nevm_ip = c['daemons'][i]['ip']
					daemons_list.append(name.upper())
					rpc_threads += 1
				except Exception as e:
					print("Config for currency {} not found. The error is {}".format(name, e))
					del c['daemons'][i]
			else:
				#others configs
				to_del_index.append(i)

				if name.upper() in ['XR_PROXY', 'SNODE', 'TNODE', 'TESTSNODE', 'TESTTNODE']:
					if name.upper() not in ['XR_PROXY']:
						customlist[0]['blocknet_image'] = c['daemons'][i]['image']
						customlist[0]['blocknet_node'] = name.lower()
					else:
						if 'image' in list(c['daemons'][i]):
							customlist[0][f'{name.lower()}_image'] = c['daemons'][i]['image']
					if f'{name.lower()}_ip' in used_ip['ip'].keys():
						customlist[0][f'{name.lower()}_ip'] = used_ip['ip'][f'{name.lower()}_ip']
					else:
						while True:
							custom_ip = autoconfig.random_ip(SUBNET)
							if custom_ip not in used_ip['ip'].values():
								customlist[0][f'{name.lower()}_ip'] = custom_ip
								used_ip['ip'][f'{name.lower()}_ip'] = custom_ip
								break
				#deploy payment configs
				if name.upper() == 'PAYMENT':
					customlist[0][f'{name.lower()}_image'] = c['daemons'][i]['image']
					if 'payment_xquery' in list(c['daemons'][i]):
						customlist[0][f'{name.lower()}_xquery'] = c['daemons'][i]['payment_xquery']
					else:
						customlist[0][f'{name.lower()}_xquery'] = 35
					if 'payment_tier1' in list(c['daemons'][i]):
						customlist[0][f'{name.lower()}_tier1'] = c['daemons'][i]['payment_tier1']
					else:
						customlist[0][f'{name.lower()}_tier1'] = 35
					if 'payment_tier2' in list(c['daemons'][i]):
						customlist[0][f'{name.lower()}_tier2'] = c['daemons'][i]['payment_tier2']
					else:
						customlist[0][f'{name.lower()}_tier2'] = 200
					customlist[0]['deploy_payment'] = True
					for k in ['PG','PAYMENT']:
						if f'{k.lower()}_ip' in used_ip['ip'].keys():
							customlist[0][f'{k.lower()}_ip'] = used_ip['ip'][f'{k.lower()}_ip']
						else:    
							while True:
								custom_ip = autoconfig.random_ip(SUBNET)
								if custom_ip not in used_ip['ip'].values():
									customlist[0][f'{k.lower()}_ip'] = custom_ip
									used_ip['ip'][f'{k.lower()}_ip'] = custom_ip
									break
					customlist[0]['plugins'].append('projects')
				if name.upper() == 'ETH':                
					customlist[0]['deploy_eth'] = True
					if 'host' in list(c['daemons'][i]):
						customlist[0]['gethexternal'] = c['daemons'][i]['host']
						print("Using external geth")
					else:
						customlist[0][f'{name.lower()}_image'] = c['daemons'][i]['image']
						print("Using internal geth")
					for k in ['GETH']:
						if f'{k.lower()}_ip' in used_ip['ip'].keys():
							customlist[0][f'{k.lower()}_ip'] = used_ip['ip'][f'{k.lower()}_ip']
						else:
							while True:
								custom_ip = autoconfig.random_ip(SUBNET)
								if custom_ip not in used_ip['ip'].values():
									if k == 'GETH' and customlist[0]['gethexternal']:
										customlist[0][f'{k.lower()}_ip'] = customlist[0]['gethexternal']
										break
									customlist[0][f'{k.lower()}_ip'] = custom_ip
									used_ip['ip'][f'{k.lower()}_ip'] = custom_ip
									break
				if name.upper() == 'AVAX':
					if 'image' in list(c['daemons'][i]):
						customlist[0][f'{name.lower()}_image'] = c['daemons'][i]['image']
						customlist[0]['deploy_avax'] = True
						print("Using internal avax")
						if f'{name.lower()}_ip' in used_ip['ip'].keys():
							customlist[0][f'{name.lower()}_ip'] = used_ip['ip'][f'{name.lower()}_ip']
						else:
							while True:
								custom_ip = autoconfig.random_ip(SUBNET)
								if custom_ip not in used_ip['ip'].values():
									customlist[0][f'{name.lower()}_ip'] = custom_ip
									used_ip['ip'][f'{name.lower()}_ip'] = custom_ip
									break
					else:
						customlist[0]['deploy_avax'] = False
						customlist[0]['avaxexternal'] = True
						customlist[0][f'{name.lower()}_ip'] = c['daemons'][i]['host']
						print("Using external avax")
				if name.upper() == 'NEVM':
					if 'image' in list(c['daemons'][i]):
						customlist[0][f'{name.lower()}_image'] = c['daemons'][i]['image']
						customlist[0]['deploy_nevm'] = True
						print("Using internal nevm")
						customlist[0]['nevm_ip'] = nevm_ip
					else:
						customlist[0]['deploy_nevm'] = False
						customlist[0]['nevmexternal'] = True
						customlist[0][f'{name.lower()}_ip'] = c['daemons'][i]['host']
						print("Using external nevm")

				if name.upper() == 'HYDRA':
					print('HYDRA exists')
					customlist[0]['plugins'].append('evm_passthrough')
					if 'free' in c['daemons'][i].keys() and c['daemons'][i]['free'] == True:
						customlist[0]['plugins'].append('free_evm_passthrough')
					for j in c['daemons'][i]['chains']:
						print(f'HYDRA - {j["name"].upper()}')
						customlist[0]['hydra'].append(j['name'].upper())
						customlist[0]['plugins'].append(f'evm_passthrough_{j["name"].lower()}')
					
				if name.upper() == 'XQUERY':
					print('XQUERY exists')
					customlist[0]['deploy_xquery'] = True
					query = dict(c['daemons'][i])
					del query['name']
					customlist[0]['plugins'].append('xquery')

					# These following two lines add names like "xquery_pangolin", "xquery_pegasys" to plugins list
					# so the specific dexes (e.g. pangolin, pegasys) supported by xquery on this SNode are broadcast to
					# the Blocknet P2P network.
					for xq_dex in query['dexs']:
						customlist[0]['plugins'].append(f'xquery_{xq_dex["name"].lower()}')

					autoconfig.write_yaml_file('xquery.yaml',query)
					used_ip, qtemplate = xq_template(used_ip, SUBNET, query, customlist[0])
					for key, item in qtemplate.items():
						c[key] = item

				if name.upper() == 'UTXO_PLUGIN':
					print('UTXO_PLUGIN exists')
					customlist[0]['deploy_utxo'] = True
					customlist[0]['utxo_plugin_volume'] = c['daemons'][i]['volume']
					customlist[0]['utxo_plugin_image'] = c['daemons'][i]['utxo_plugin_image']
					customlist[0]['plugin_adapter_image'] = c['daemons'][i]['plugin_adapter_image']
					if name in used_ip['ip'].keys():
						customlist[0]['plugin_adapter_ip'] = used_ip['ip'][name]
					else:
						while True:
							custom_ip = autoconfig.random_ip(SUBNET)
							if custom_ip not in used_ip['ip'].values():
								customlist[0]['plugin_adapter_ip'] = custom_ip
								used_ip['ip']['plugin_adapter_ip'] = custom_ip
								break

#					utxo_plugin = dict(c['daemons'][i])
					customlist[0]['plugins'] += UTXO_PLUGIN_METHODS
					customlist[0]['utxo_plugin_methods'] = UTXO_PLUGIN_METHODS
					used_ip, utxotemplate = utxo_template(used_ip, SUBNET, c['daemons'][i], customlist[0])
					for key, item in utxotemplate.items():
						c[key] = item

				#volumes paths configs
				for j in list(c['daemons'][i]):
					if j not in ['name','image']:
						mount_dir = f'{name.lower()}_{j}'
						customlist[0][mount_dir] = os.environ.get(mount_dir.upper(),c['daemons'][i][j])

		write_text_file(IPS_CACHE,json.dumps(used_ip, indent=4, sort_keys=False))
		#check for missed configs
		#loading template vars
		template_vars = autoconfig.template_vars('autobuild/templates/{}'.format(c['j2template']))
		# print("template_vars:",template_vars)
		# print("c['daemons']:",c['daemons'])
		# print(daemons_list)
		# for index, var in enumerate(c['daemons']):
		#     #check if fake daemon or not (SNODE ETH XR_PROXY)
		#     if var['name'] in daemons_list:
		#         #compare daemons with template
		#         tocomp_a = list(var)
		#         tocomp_b = list(template_vars['daemons'])
		#         tocomp_a.sort()
		#         tocomp_b.sort()
		#         print(tocomp_a)
		#         print(tocomp_b)
		#         if set(tocomp_b).issubset(tocomp_a) == False:
		#             #if daemons missing config add to to_del_index
		#             print(f'invalid config in YAML for {var["name"]}:\nmissing {list(set(tocomp_a).symmetric_difference(set(tocomp_b)))}')
		#             to_del_index.append(index)

		#     elif var['name'].upper() in ['XR_PROXY', 'SNODE', 'TNODE', 'TESTSNODE', 'ETH', 'XQUERY', 'AVAX', 'PAYMENT']:
		#         continue

		#delete fake daemons SNODE ETH XR_PROXY
		to_del_index.sort(reverse=True)
		for i in to_del_index:
			del c['daemons'][i]

		if rpc_threads > 4:
			c['rpcthreads'] = rpc_threads * 2
		else:
			c['rpcthreads'] = 8

		custom_template_fname = 'autobuild/templates/{}'.format(c['j2template'])
		with open(custom_template_fname,'r') as file:
			template_string = file.read()
		custom_template = J2_ENV.from_string(template_string)
		# custom_template = J2_ENV2.get_template(custom_template_fname)
		rendered_data = custom_template.render(c)
		rendered_filename = '{}{}.yml'.format(OUTPUT_PATH, c['name'])
		write_text_file(rendered_filename, rendered_data)

		plugins = ''
		if len(customlist[0]['plugins']) >= 1:
			for i in customlist[0]['plugins']:
				plugins = plugins + i +','
			plugins = plugins[:-1]

		customlist[0]['xrouter_plugins'] = plugins
		customlist[0]['hydra'] = ','.join([x.upper() for x in customlist[0]['hydra']])

		return([c])


def processconfigs(datalist, BRANCHPATH):
	if(datalist[0]["blocknet_node"].upper() in ['SNODE', 'TNODE']):
		base_block = 'BLOCK'
	else:
		base_block = 'TBLOCK'

	XBRIDGE_CONF = "[Main]\nFullLog=true\nLogPath=\nExchangeTax=300\nExchangeWallets="+base_block+","

	custom_template_ec = J2_ENV.get_template('autobuild/templates/entrypoint_config.j2')

	for data in datalist:
		for daemon in data['daemons']:
			name = daemon['name']
			if name.upper() not in ['TNODE', 'SNODE', 'TESTSNODE', 'TESTTNODE', 'ETH', 'XR_PROXY']:
				XBRIDGE_CONF += "{},".format(name)
				if 'rpcserialversion' in daemon:
					template_wc = Template(autoconfig.load_template(autoconfig.wallet_config(BRANCHPATH))).render(
                        			p2pPort=daemon['p2pPort'], rpcPort=daemon['rpcPort'], legacy=daemon['legacy'],
                       				deprecatedrpc=daemon['deprecatedrpc'], rpcserialversion=daemon['rpcserialversion'], )
				else:
					template_wc = Template(autoconfig.load_template(autoconfig.wallet_config(BRANCHPATH))).render(
                       				p2pPort=daemon['p2pPort'], rpcPort=daemon['rpcPort'], legacy=daemon['legacy'],deprecatedrpc=daemon['deprecatedrpc'], )
				if name == 'SYS' and datalist[0]['deploy_nevm'] is True:
					write_nevm = True
					nevm_ip = datalist[0]['nevm_ip']
				else:	 
					write_nevm = False
					nevm_ip = '0.0.0.0'
				rendered_data_ec = custom_template_ec.render({'walletConfig': template_wc,
															  'configName': daemon['configName'],
															  'writeNEVM': write_nevm,
															  'nevmIP': nevm_ip})
				config_name = './scripts/entrypoints/start-{}.sh'.format(daemon['configName'])
				print('Creating File: {}'.format(config_name))
				autoconfig.save_config(rendered_data_ec, config_name)
				st = os.stat(config_name)
				os.chmod(config_name, st.st_mode | stat.S_IEXEC)

	XBRIDGE_CONF = XBRIDGE_CONF[:-1]
	XBRIDGE_CONF += '\n\n'

	XR_TOKENS = base_block
	for data in datalist:
		p2pport = ''
		rpcport = ''
		username = os.environ.get("RPC_USER", "${RPC_USER}")
		password = os.environ.get("RPC_PASSWORD", "${RPC_PASSWORD}")
		for daemon in data['daemons']:
			name = daemon['name']
			ip = daemon['ip']
			if name.upper() not in ['TNODE', 'SNODE', 'TESTSNODE', 'TESTTNODE', 'ETH', 'XR_PROXY']:
				XR_TOKENS += ','+name.upper()
				XBRIDGE_CONF += "{}\n\n".format(autoconfig.generate_confs(BRANCHPATH, name, p2pport, rpcport, username, password, ip))
				print('Add Xbridge: {}'.format(name))
		# Add BLOCK settings
		XBRIDGE_CONF += "{}\n\n".format(autoconfig.generate_confs(BRANCHPATH, base_block, p2pport, rpcport, username, password, '127.0.0.1'))

	autoconfig.save_config(XBRIDGE_CONF, os.path.join('./scripts/config', 'xbridge.conf'))
	custom_template_xr = J2_ENV.get_template('autobuild/templates/xrouter.j2')
	XROUTER_CONF = custom_template_xr.render({'XR_TOKENS': XR_TOKENS, 'xrouter_plugins': datalist[0]['xrouter_plugins']})

	custom_template_snode = J2_ENV.get_template(f'autobuild/templates/{datalist[0]["blocknet_node"]}.j2')
	datalist[0]['XROUTER_CONF'] = XROUTER_CONF
	datalist[0]['XBRIDGE_CONF'] = XBRIDGE_CONF
	rendered_data_snode = custom_template_snode.render(datalist[0])
	autoconfig.save_config(rendered_data_snode, f'./scripts/start-{datalist[0]["blocknet_node"]}.sh')

	custom_template_uw = J2_ENV.get_template('autobuild/templates/xrproxy.j2')
	rendered_data_uw = custom_template_uw.render(datalist[0])
	autoconfig.save_config(rendered_data_uw, './scripts/start-xrproxy.sh')
	autoconfig.make_executable_files('./scripts')
	autoconfig.make_executable_files('./scripts/entrypoints')

	

