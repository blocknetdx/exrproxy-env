#!/usr/bin/env python3
from autobuild.utils import *
from autobuild.app import processcustom, processconfigs
from autobuild.utils.autoconfig import write_text_file, write_yaml_file, write_json_file, load_yaml_file, load_json_file, load_text_file
import autobuild.utils.autoconfig
import argparse, re, psutil, os, socket, logging
from datetime import datetime
from rich import print
from rich.table import Table
from rich import pretty
from dotenv import dotenv_values
import subprocess

# Global vars
branchpath = re.sub(r'(^(?!.*/$).*)',r'\1/','https://raw.githubusercontent.com/blocknetdx/blockchain-configuration-files/master')
KNOWN_HOSTS_FILE = '.known_hosts'
KNOWN_VOLUMES = '.known_volumes'
ENV_FILE = '.env'
CACHE = '.cache'
ABI = 'abi'

# Install pretty prints
pretty.install()
xrouter_emoticon = ":twisted_rightwards_arrows:"
app_title = f'{xrouter_emoticon} [bold cyan]EXRPROXY-ENV[/bold cyan] [bold red]BUILDER[/bold red]'

# Resources table
virtual_memory = psutil.virtual_memory()
virtual_memory = {'total':virtual_memory.total,'used':virtual_memory.used,'used%':virtual_memory.percent,'free':virtual_memory.total-virtual_memory.used,'free%':100-virtual_memory.percent}
hw_table = Table(title='',box=None)
hw_table.add_column('',justify='left', style='bold green', no_wrap=False)
hw_table.add_column('Hardware',justify='left', style='bold green', no_wrap=True)
hw_table.add_column('Size',justify='left', style='bold yellow', no_wrap=True)
hw_table.add_column('Used',justify='left', style='bold red', no_wrap=True)
hw_table.add_column('%',justify='left', style='bold red', no_wrap=True)
hw_table.add_column('Free',justify='left', style='bold green', no_wrap=True)
hw_table.add_column('%',justify='left', style='bold green', no_wrap=True)
hw_table.add_row(app_title, 'CPU', str(psutil.cpu_count())) #CPU CORES
hw_table.add_row('', 'RAM','{:.2f}GB'.format(round(virtual_memory['total']/ (1024.0 **3))),'{:.2f}GB'.format(round(virtual_memory['used']/ (1024.0 **3))),'{:.2f}%'.format(virtual_memory['used%']),'{:.2f}GB'.format(round(virtual_memory['free']/ (1024.0 **3))),'{:.2f}%'.format(virtual_memory['free%']))
for mount_point in [x.mountpoint for x in psutil.disk_partitions(all=False)]:
	hw_table.add_row(mount_point, 'DISK', '{:.2f}GB'.format(psutil.disk_usage(mount_point).total / (2**30)), '{:.2f}GB'.format(psutil.disk_usage(mount_point).used / (2**30)),'{:.2f}%'.format(psutil.disk_usage(mount_point).percent),'{:.2f}GB'.format(psutil.disk_usage(mount_point).free / (2**30)),'{:.2f}%'.format(100-psutil.disk_usage(mount_point).percent))

# CLI arguments
parser = argparse.ArgumentParser()
parser.add_argument('--nochecks', help="Don't check docker requirements", action='store_true')
parser.add_argument('--noenv', help="Don't check if .env file exists (only for advanced users)", action='store_true')
parser.add_argument('--deploy', help='Autodeploy stack', default=False, action='store_true')
parser.add_argument('--prune', help='Prune docker', default=False, action='store_true')
parser.add_argument('--source', help='Source file', default='autobuild/sources.yaml')
parser.add_argument('--yaml', help='Custom input yaml', default=False)
parser.add_argument('--interval', help='Docker stopping interval till sends SIGKILL signal; default 30s', default=30)
parser.add_argument('--branchpath', default=branchpath)
parser.add_argument('--prunecache', help='Reinit .known_hosts, .known_volumes, .env and .cache files', action='store_true')
parser.add_argument('--subnet', help='Subnet to configure docker-compose network', default="172.31.0.0/20")

args = parser.parse_args()
SOURCE = args.source
YAML = args.yaml
CHECKS = args.nochecks
ENV = args.noenv
DEPLOY = args.deploy
PRUNE = args.prune
BRANCHPATH = args.branchpath
STOP_INTERVAL = int(args.interval)
PRUNE_CACHE = args.prunecache
SUBNET = args.subnet

# Delete cache files
if PRUNE_CACHE:
	os.remove(KNOWN_HOSTS_FILE)
	os.remove(KNOWN_VOLUMES)
	os.remove(ENV_FILE)
	os.remove(CACHE)

# Redownload abi dir from XQuery
if ABI in os.listdir(os.getcwd()):
	proc = subprocess.Popen(['rm', '-rf', 'abi'], shell=False)
	proc.wait()
proc = subprocess.Popen(['gitdir', 'https://github.com/blocknetdx/XQuery/tree/master/abi'], shell=False)
proc.wait()

# Create .env
if ENV_FILE not in os.listdir(os.getcwd()):
	data = "PUBLIC_IP=\nSN_NAME=\nSN_KEY=\nSN_ADDRESS=\nRPC_USER=\nRPC_PASSWORD="
	write_text_file(ENV_FILE,data)

# Create .known_hosts
if KNOWN_HOSTS_FILE not in os.listdir(os.getcwd()):
	data = {'hosts':{}}
	write_text_file(KNOWN_HOSTS_FILE,json.dumps(data, indent=4, sort_keys=False))

# Create .known_volumes
if KNOWN_VOLUMES not in os.listdir(os.getcwd()):
	data = {'volumes':{}}
	write_text_file(KNOWN_VOLUMES,json.dumps(data, indent=4, sort_keys=False))

# Create .cache
if CACHE not in os.listdir(os.getcwd()):
	data = {'ticks':[],'payment_tier1':None,'payment_tier2':None,'discount_ablock':None,'discount_aablock':None}
	write_text_file(CACHE,json.dumps(data, indent=4, sort_keys=False))

# Load config files
dirname = os.path.basename(os.getcwd())
print(f'Working Directory [bold red]{os.getcwd()}[/bold red]')
source = load_yaml_file(SOURCE)
known_hosts = json.loads(load_text_file(KNOWN_HOSTS_FILE))
known_volumes = json.loads(load_text_file(KNOWN_VOLUMES))
cache = json.loads(load_text_file(CACHE))

if __name__ == '__main__':
	print(hw_table)
	print()
	# Create Snode instance
	snode = Snode(dirname, ENV_FILE)

	try:
		# Prune docker and exit
		if PRUNE:
			print(f"[bold magenta]{'-'*50}[/bold magenta]")
			snode.docker_prune()
		# Requirements checks
		if not CHECKS:
			print(f"[bold magenta]{'-'*50}[/bold magenta]")
			snode.checks(STOP_INTERVAL)
		# Set env vars
		if not ENV:
			print(f"[bold magenta]{'-'*50}[/bold magenta]")
			snode.env_vars()
		dot_env_values = dotenv_values(".env")
		
		if not YAML:
			# Get sudo pass
			print(f"[bold magenta]{'-'*50}[/bold magenta]")
			snode.get_sudo()

			# Parse sources.yaml categories
			base = [x for x in source if x['type']=='base']
			chains = [x for x in source if x['type']=='chain']
			evm_chains = [x for x in source if x['type']=='evm_chain']
			apps = [x for x in source if x['type']=='app']
			print(f"[bold magenta]{'-'*50}[/bold magenta]")
			# Start inquirer
			chains_todeploy = snode.inquirer.pick_checkbox("What chains for XBridge do you wish to support?",[{'name':f"{str(x['name']).ljust(4,' ')} | RAM {str(x['ram']).ljust(4,' ')} GB | CPU {str(x['cpu']).ljust(4,' ')} Cores | DISK {str(x['disk']).ljust(6,' ')} GB | {x['volume'] if x['name'] not in known_volumes['volumes'].keys() else known_volumes['volumes'][x['name']]}",'checked':True if x['name'] in cache['ticks'] else False} for x in chains])
			for cd in chains_todeploy:
				cd = cd.split(' ')[0]
				for c in chains:
					if cd == c['name']:
						if c['name'] in known_volumes['volumes'].keys():
							c['volume'] = known_volumes['volumes'][c['name']]
						input_template[0]['daemons'].append(c)
			print(f"[bold magenta]{'-'*50}[/bold magenta]")			
			evm_chains_todeploy = snode.inquirer.pick_checkbox("What EVM chains do you wish to support?",[{'name':f"{str(x['name']).ljust(4,' ')} | RAM {str(x['ram']).ljust(4,' ')} GB | CPU {str(x['cpu']).ljust(4,' ')} Cores | DISK {str(x['disk']).ljust(6,' ')} GB | {x['volume'] if x['name'] not in known_volumes['volumes'].keys() else known_volumes['volumes'][x['name']]}",'checked':True if x['name'] in cache['ticks'] else False} for x in evm_chains])
			for evcd in evm_chains_todeploy:
				evcd = evcd.split(' ')[0]
				for evc in evm_chains:
					if evcd == evc['name']:						
						if evcd in known_hosts['hosts'].keys():
							hosts = known_hosts['hosts'][evcd]
							location = snode.inquirer.pick_one(f'Select one host for {evcd}',hosts+['New external host','Internally'])
							if location == 'New external host':
								location = snode.inquirer.get_input(f"Press enter external IP Address for {evcd}:")
								if location not in ['',' '] and location not in hosts:
									known_hosts['hosts'][evcd].append(location)
						else:
							location = snode.inquirer.get_input(f"Press enter to use {evcd} internally or type external IP Address:")
						if location not in ['',' ','Internally']:
							external = {"name":evcd,"host":location}
							if not evcd in known_hosts['hosts'].keys():
								known_hosts['hosts'][evcd] = [location]
							elif location not in known_hosts['hosts'][evcd]:
								known_hosts['hosts'][evcd].append(location)
							input_template[0]['daemons'].append(external)
						else:
							if evcd == 'AVAX':
								evc['public_ip'] = socket.gethostbyname(dot_env_values['PUBLIC_IP'])
							if evcd in known_volumes['volumes'].keys():
								evc['volume'] = known_volumes['volumes'][evcd]
							input_template[0]['daemons'].append(evc)
			write_text_file(KNOWN_HOSTS_FILE,json.dumps(known_hosts, indent=4, sort_keys=False))
			print(f"[bold magenta]{'-'*50}[/bold magenta]")
			if len(evm_chains_todeploy)>0:
				apps_counts = 0
				for app in apps:
					name = app['name']
					app_check = snode.inquirer.ask_question(f"Do you wish to support {app['name']} | RAM {app['ram']} GB | CPU {app['cpu']} Cores | DISK {app['disk']} GB ?", default=True if app['name'] in cache['ticks'] else False)
					if app_check == True:
						app_chains = snode.inquirer.pick_checkbox(f"Select EVM chains to attach {name} to:",[{'name':x.split(' ')[0],'checked':True if name in cache['ticks'] else False} for x in evm_chains_todeploy])
						# app_chains = [x.split(' ')[0] for x in app_chains]
						if len(app_chains)==0:
							print(f'{name} ignored... No selection.')
						else:
							if name == 'HYDRA':
								hydra_config = {'name':name,'free':False, 'chains':[{'name':x} for x in app_chains]}
								# free_access = snode.inquirer.ask_question(f"Do you wish to support FREE access to {name}?",default=False)
								# if free_access != True:
								# 	hydra_config['free'] = True
								apps_counts += 1
								input_template[0]['daemons'].append(hydra_config)
							if name == 'XQUERY':
								indices = []
								for evm_chain in app_chains:
									indexers = snode.inquirer.pick_checkbox(f'Select which indices you want for {evm_chain}:',[{'name':'_'.join(x['name'].split('_')[1::]),'checked':True if x['name'] in cache['ticks'] else False} for x in app['chains'] if evm_chain in x['name']])
									if len(indexers) == 0:
										print(f'{evm_chain} ignored for {name}...No selection.')
									else:
										for index in app['chains']:
											for i in indexers:
												if i in index['name']:
													indices.append(index)
								if len(indices) == 0:
									print(f'{name} ignored... No selection.')
								else:
									app['chains'] = indices
									if name in known_volumes['volumes'].keys():
										app['volume'] = known_volumes['volumes'][name]
									apps_counts += 1
									input_template[0]['daemons'].append(app)
				if apps_counts == 0:
					print('[bold red]No EVM chain app configured. Removing EVM chains...[/bold red]')
					for evm in evm_chains:
						for entry in input_template[0]['daemons']:
							if entry['name'] == evm['name']:
								input_template[0]['daemons'].remove(entry)
								print(f'Removed [bold red]{evm["name"]}[/bold red]')
			for b in base:				
				if b['name'] == 'PAYMENT' and any([[True for x in [deploy['name'] for deploy in input_template[0]['daemons']] if x==xx] for xx in [echain['name'] for echain in evm_chains]]):
					print(f"[bold magenta]{'-'*50}[/bold magenta]")
					if cache["payment_tier1"]:
						b['payment_tier1'] = cache["payment_tier1"]
					if cache["payment_tier2"]:
						b['payment_tier2'] = cache["payment_tier2"]
					if cache["discount_ablock"]:
						b['discount_ablock'] = cache["discount_ablock"]
					if cache["discount_aablock"]:
						b['discount_aablock'] = cache["discount_aablock"]
					tier1 = snode.inquirer.get_input(f'Press enter for {b["payment_tier1"]}USD tier1 amount or type a new USD price:')
					b['payment_tier1'] = int(tier1) if tier1 !='' else b["payment_tier1"]
					tier2 = snode.inquirer.get_input(f'Press enter for {b["payment_tier2"]}USD tier2 amount or type a new USD price:')
					b['payment_tier2'] = int(tier2) if tier2 !='' else b["payment_tier2"]
					ablock_discount = snode.inquirer.get_input(f'Press enter for {b["discount_ablock"]}% aBLOCK discount or type a new discount (e.g. 15 for 15% aBLOCK discount):')
					b['discount_ablock'] = int(ablock_discount) if ablock_discount !='' else b["discount_ablock"]
					aablock_discount = snode.inquirer.get_input(f'Press enter for {b["discount_aablock"]}% aaBLOCK discount or type a new discount (e.g. 15 for 15% aaBLOCK discount):')
					b['discount_aablock'] = int(aablock_discount) if aablock_discount !='' else b["discount_aablock"]
				if b['name'] in known_volumes['volumes'].keys():
					b['volume'] = known_volumes['volumes'][b['name']]
				if b['name'] != 'PAYMENT':
					input_template[0]['daemons'].append(b)
				elif any([[True for x in [deploy['name'] for deploy in input_template[0]['daemons']] if x==xx] for xx in [echain['name'] for echain in evm_chains]]):
					input_template[0]['daemons'].append(b)
			print(f"[bold magenta]{'-'*50}[/bold magenta]")		
			answer = snode.inquirer.ask_question('Do you wish to change install locations?', default=False)
			if answer == True:
				volumes = [{'name':x['name'],'volume':x['volume'],'disk':x['disk']} for x in input_template[0]['daemons'] if 'volume' in x.keys()]
				answer = snode.inquirer.pick_checkbox('Select to which entries you wish to change install location:',[{'name':f"{x['name']} {x['volume']}",'checked':False} for x in volumes])
				if len(answer) == 0:
					print(f'Location change ignored... No selection.')
					snode.comparedisksize([x['name'] for x in input_template[0]['daemons'] if 'volume' in x.keys()], [x['volume'] for x in input_template[0]['daemons'] if 'volume' in x.keys()], [x['disk'] for x in input_template[0]['daemons'] if 'volume' in x.keys()])
				else:
					for entry in answer:
						not_abs_path = False
						entry_answer = ''
						while not not_abs_path:
							entry_answer = snode.inquirer.get_input(f'Press enter to confirm {entry} or type a new absolute path:')
							if entry_answer == '':
								not_abs_path = True
							elif os.path.isabs(entry_answer) == True:
								not_abs_path = True
							else:
								print(f'[bold red]{entry_answer}[/bold red] is not a [bold yellow]absolute path[/bold yellow]... try again')
						for i, e in enumerate(input_template[0]['daemons']):
							if e['name'] == entry.split(' ')[0]:
								if entry_answer == '':
									entry_answer = input_template[0]['daemons'][i]['volume']
								input_template[0]['daemons'][i]['volume'] = entry_answer
								known_volumes['volumes'][e['name']] =  entry_answer
								snode.comparedisksize([entry.split(' ')[0]], [entry_answer], [input_template[0]['daemons'][i]['disk']])
				print('[bold yellow]Updated install locations[/bold yellow]')
				snode.comparedisksize([x['name'] for x in input_template[0]['daemons'] if 'volume' in x.keys()], [x['volume'] for x in input_template[0]['daemons'] if 'volume' in x.keys()], [x['disk'] for x in input_template[0]['daemons'] if 'volume' in x.keys()])
				used_volumes = set([x['volume'] for x in input_template[0]['daemons'] if 'volume' in x.keys()])
				for volume in used_volumes:
					required = sum([x['disk'] for x in input_template[0]['daemons'] if 'volume' in x.keys() and x['volume']==volume])
					snode.comparedisksize(['TOTAL'], [volume], [required])
			else:
				print('[bold yellow]Updated install locations[/bold yellow]')
				snode.comparedisksize([x['name'] for x in input_template[0]['daemons'] if 'volume' in x.keys()], [x['volume'] for x in input_template[0]['daemons'] if 'volume' in x.keys()], [x['disk'] for x in input_template[0]['daemons'] if 'volume' in x.keys()])
				used_volumes = set([x['volume'] for x in input_template[0]['daemons'] if 'volume' in x.keys()])
				for volume in used_volumes:
					required = sum([x['disk'] for x in input_template[0]['daemons'] if 'volume' in x.keys() and x['volume']==volume])
					snode.comparedisksize(['TOTAL'], [volume], [required])
			write_text_file(KNOWN_VOLUMES,json.dumps(known_volumes, indent=4, sort_keys=False))
			print(f"[bold magenta]{'-'*50}[/bold magenta]")
			now = datetime.now().strftime("%d-%m-%Y-%H:%M")
			config_name = snode.inquirer.get_input(f"Press enter to save config as {now} or enter name:")
			for app in input_template[0]['daemons']:
				for to_del in ['disk','ram','cpu']:
					if to_del in app.keys():
						del app[to_del]
			if config_name == '':
				write_yaml_file(f'inputs_yaml/{now}.yaml',input_template)
			else:
				write_yaml_file(f'inputs_yaml/{config_name}.yaml',input_template)
			cache = {'ticks':[],'payment_tier1':None,'payment_tier2':None,'discount_ablock':None,'discount_aablock':None}
			for daemon in input_template[0]['daemons']:
				cache['ticks'].append(daemon['name'])
				if daemon['name'] == 'PAYMENT':
					cache['payment_tier1'] = daemon['payment_tier1']
					cache['payment_tier2'] = daemon['payment_tier2']
					cache['discount_ablock'] = daemon['discount_ablock']
					cache['discount_aablock'] = daemon['discount_aablock']
				if daemon['name'] == 'XQUERY':
					for index in daemon['chains']:
						cache['ticks'].append(index['name'])
			write_text_file(CACHE,json.dumps(cache, indent=4, sort_keys=False))
		else:
		# Parse input yaml if given as CLI arg	
			input_template = load_yaml_file(YAML)
			if input_template == "ERROR":
				print(f"Error loading {YAML}")
				sys.exit(0)

		input_template_args[0]['daemons'] = input_template[0]['daemons']
		data_with_ips = processcustom(input_template_args, SUBNET, BRANCHPATH)
		processconfigs(data_with_ips, BRANCHPATH)
		
		# Deploy snode config
		if DEPLOY:
			snode.deploy()

		snode.atexit()
	except Exception as e:
		logging.critical('Exception:',exc_info=True)
		snode.atexit()
	except KeyboardInterrupt:
		snode.atexit()


