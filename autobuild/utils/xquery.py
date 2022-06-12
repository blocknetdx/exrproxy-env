import ipaddress
from autobuild.utils.autoconfig import random_ip

def xq_template(used_ip, subnet, query, data):

	# subnet = '172.31.0.0/20'
	
	# ips = [str(ip) for ip in ipaddress.IPv4Network(subnet)][2::]
	hasura_port = 8080
	postgres_port = 5432
	gateway_port1 = 5555
	gateway_port2 = 5556
	reverse_proxy_port = 81
	
	final_data = {}
	final_data['chains'] = []
	for key0, item0 in query.items():
		if key0 == 'chains':
			for item in item0:
				name = item['name']
				if 'AVAX' in name:
					item['rpc_host'] = f"http://{data['avax_ip']}:9650/ext/bc/C/rpc"
				if 'ETH' in name:
					item['rpc_host'] = f"http://{data['geth_ip']}:8545"
				item['query'] = [dict(t) for t in {tuple(d.items()) for d in item['query']}]
				if name in used_ip['ip'].keys():
					item['ip'] = used_ip['ip'][name]
				else:
					while True:
						custom_ip = random_ip(subnet)
						if custom_ip not in used_ip['ip'].values():
							item['ip'] = custom_ip
							used_ip['ip'][name] = custom_ip
							break
				final_data['chains'].append(item)
		elif key0 == 'graph':
			final_data[key0] = item0
		elif key0 == 'endpoint':
			final_data[key0] = item0

	if 'postgres_ip' in used_ip['ip'].keys():
		final_data['postgres_ip'] = used_ip['ip']['postgres_ip']
	else:
		while True:
			custom_ip = random_ip(subnet)
			if custom_ip not in used_ip['ip'].values():
				final_data['postgres_ip'] = custom_ip
				used_ip['ip']['postgres_ip'] = custom_ip
				break
	final_data['postgres_port'] = str(postgres_port)
	if 'gateway_processor_ip' in used_ip['ip'].keys():
		final_data['gateway_processor_ip'] = used_ip['ip']['gateway_processor_ip']
	else:
		while True:
			custom_ip = random_ip(subnet)
			if custom_ip not in used_ip['ip'].values():
				final_data['gateway_processor_ip'] = custom_ip
				used_ip['ip']['gateway_processor_ip'] = custom_ip
				break
	final_data['gateway_processor_port1'] = str(gateway_port1)
	final_data['gateway_processor_port2'] = str(gateway_port2)
	if 'db_processor_ip' in used_ip['ip'].keys():
		final_data['db_processor_ip'] = used_ip['ip']['db_processor_ip']
	else:
		while True:
			custom_ip = random_ip(subnet)
			if custom_ip not in used_ip['ip'].values():
				final_data['db_processor_ip'] = custom_ip
				used_ip['ip']['db_processor_ip'] = custom_ip
				break
	if 'graphql_engine_ip' in used_ip['ip'].keys():
		final_data['graphql_engine_ip'] = used_ip['ip']['graphql_engine_ip']
	else:
		while True:
			custom_ip = random_ip(subnet)
			if custom_ip not in used_ip['ip'].values():
				final_data['graphql_engine_ip'] = custom_ip
				used_ip['ip']['graphql_engine_ip'] = custom_ip
				break
	final_data['graphql_engine_port'] = str(hasura_port)
	if 'reverse_proxy_ip' in used_ip['ip'].keys():
		final_data['reverse_proxy_ip'] = used_ip['ip']['reverse_proxy_ip']
	else:
		while True:
			custom_ip = random_ip(subnet)
			if custom_ip not in used_ip['ip'].values():
				final_data['reverse_proxy_ip'] = custom_ip
				used_ip['ip']['reverse_proxy_ip'] = custom_ip
				break
	final_data['reverse_proxy_port'] = reverse_proxy_port
	final_data['query_config'] = 'xquery.yaml'
	
	return [used_ip, final_data]
