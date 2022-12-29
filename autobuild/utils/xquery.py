import os
import ipaddress
from autobuild.utils.autoconfig import random_ip

def xq_template(used_ip, subnet, query, data):

	# subnet = '172.31.0.0/20'
	
	# ips = [str(ip) for ip in ipaddress.IPv4Network(subnet)][2::]
	hasura_port = 8080
	postgres_port = 5432
	redis_port = 6379
    
	final_data = {}
	final_data['dexs'] = []
	for key0, item0 in query.items():
		if key0 == 'dexs':
			redis_db = 0
			for item in item0:
				item['redis_db'] = redis_db
				item['alembic_sleep'] = int(redis_db * 5) # make sure two xq-engine containers don't run alembic concurrently
				redis_db += 1
				name = item['name'].upper()
				if 'AVAX' in name:
					item['rpc_host'] = f"http://{data['avax_ip']}:9650/ext/bc/C/rpc"
					if 'PANGOLIN' in name:
						item['schema_name'] = 'png'
				if 'ETH' in name:
					item['rpc_host'] = f"http://{data['geth_ip']}:8545"
					if 'UNISWAP' in name:
						if 'V2' in name:
							item['schema_name'] = 'univ2'
						if 'V3' in name:
							item['schema_name'] = 'univ3'
				if 'NEVM' in name:
					item['rpc_host'] = f"http://{data['nevm_ip']}:8545"
					if 'PEGASYS' in name:
						item['schema_name'] = 'psys'
				if name in used_ip['ip'].keys():
					item['ip'] = used_ip['ip'][name]
				else:
					while True:
						custom_ip = random_ip(subnet)
						if custom_ip not in used_ip['ip'].values():
							item['ip'] = custom_ip
							used_ip['ip'][name] = custom_ip
							break

				final_data['dexs'].append(item)

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

	if 'redis_ip' in used_ip['ip'].keys():
		final_data['redis_ip'] = used_ip['ip']['redis_ip']
	else:
		while True:
			custom_ip = random_ip(subnet)
			if custom_ip not in used_ip['ip'].values():
				final_data['redis_ip'] = custom_ip
				used_ip['ip']['redis_ip'] = custom_ip
				break
	final_data['redis_port'] = str(redis_port)

	if 'hasura_ip' in used_ip['ip'].keys():
		final_data['hasura_ip'] = used_ip['ip']['hasura_ip']
	else:
		while True:
			custom_ip = random_ip(subnet)
			if custom_ip not in used_ip['ip'].values():
				final_data['hasura_ip'] = custom_ip
				used_ip['ip']['hasura_ip'] = custom_ip
				break
	final_data['hasura_port'] = str(hasura_port)

	final_data['xq_num_workers'] = os.cpu_count()
	
	return [used_ip, final_data]
