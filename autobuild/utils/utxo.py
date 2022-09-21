from rich import print
from autobuild.utils.autoconfig import random_ip

def utxo_template(used_ip, subnet, utxo_plugin, data):

	# create dictionary to access utxo coin RPC port and container IP address
	utxo_coin_dict = {'BLOCK':{'ip':data['snode_ip'],'rpc_port':'41414'}}
	utxo_coins = [x['name'] for x in utxo_plugin['chains']]
	for daemon in data['daemons']:
		if daemon['name'] in utxo_coins:
			utxo_coin_dict[daemon['name']] = {'ip':daemon['ip'], 'rpc_port':daemon['rpcPort']}

	# prepare data to fill in utxo plugin container data in autobuild/templates/utxo.j2
#	print("utxo_coin_dict: ", utxo_coin_dict)
#	print("utxo_plugin: ", utxo_plugin)
#	print("data: ", data)
	final_data = {}
	final_data['full_utxo_plugin_chains'] = []
	utxo_container_ip = {}
	for coin_name in utxo_coins:
		utxo_plugin_chain = {'name':coin_name}
		ip_name = f'{coin_name.lower()}_utxo_plugin_ip'
		custom_ip = random_ip(subnet)
		if ip_name in used_ip['ip'].keys():
			utxo_plugin_chain['ip'] = used_ip['ip'][ip_name]
		else:
			while True:
				custom_ip = random_ip(subnet)
				if custom_ip not in used_ip['ip'].values():
					utxo_plugin_chain['ip'] = custom_ip
					used_ip['ip'][ip_name] = custom_ip
					break
		utxo_container_ip[coin_name] = utxo_plugin_chain['ip']
		utxo_plugin_chain['rpc_port'] = utxo_coin_dict[coin_name]['rpc_port']
		utxo_plugin_chain['daemon_addr'] = utxo_coin_dict[coin_name]['ip']
		utxo_plugin_chain['depends_on'] = coin_name if coin_name != 'BLOCK' else 'snode'
		final_data['full_utxo_plugin_chains'].append(utxo_plugin_chain)

	# prepare data to fill in plugin adapter container data in autobuild/templates/utxo.j2
	final_data['adapter_utxo_plugin_list'] = ','.join([f'{coin_name}:{utxo_container_ip[coin_name]}' for coin_name in utxo_coins])

	return [used_ip, final_data]
