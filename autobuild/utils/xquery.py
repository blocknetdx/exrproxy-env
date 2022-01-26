import ipaddress

def xq_template(query, data):

	subnet = '172.31.0.0/20'
	
	ips = [str(ip) for ip in ipaddress.IPv4Network(subnet)][2::]
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
				item['ip'] = ips.pop(0)
				final_data['chains'].append(item)
		elif key0 == 'graph':
			final_data[key0] = item0
		elif key0 == 'endpoint':
			final_data[key0] = item0

	final_data['postgres_ip'] = ips.pop(0)
	final_data['postgres_port'] = str(postgres_port)
	final_data['gateway_processor_ip'] = ips.pop(0)
	final_data['gateway_processor_port1'] = str(gateway_port1)
	final_data['gateway_processor_port2'] = str(gateway_port2)
	final_data['db_processor_ip'] = ips.pop(0)
	final_data['graphql_engine_ip'] = ips.pop(0)
	final_data['graphql_engine_port'] = str(hasura_port)
	final_data['reverse_proxy_ip'] = ips.pop(0)
	final_data['reverse_proxy_port'] = reverse_proxy_port
	final_data['query_config'] = 'xquery.yaml'
	
	return final_data
