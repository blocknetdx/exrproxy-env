from rich import print
from rich.table import Table
import math
import docker
import sys
import os
import subprocess
import requests
import yaml
import json
import dotenv
import socket
import psutil
import pathlib
from packaging import version
from PyInquirer import style_from_dict, Token, prompt

input_template = [{
	'daemons': []
}]

input_template_args = [{
	'j2template': 'dockercompose.j2',
	'name': 'docker-compose',
	'plugins': [],
	'hydra': [],
	'deploy_eth': False,
	'gethexternal': False,
	'eth_testnet': False,
	'syncmode': 'light'
}]


class Inquirer():
	def __init__(self):
		self.style = style_from_dict({
			Token.Separator: '#cc5454 bold',
			Token.QuestionMark: '#cc5454 bold',
			Token.Selected: '#00ff00 bold',
			Token.Pointer: '#673ab7 bold',
			Token.Instruction: '',
			Token.Answer: '#f44336 bold',
			Token.Question: '',
		})

	def pick_checkbox(self,ask,choices):
		que = [
			{
				'type': 'checkbox',
				'message': ask,
				'name': 'input',
				'choices': choices,
			}]
		answer = prompt(que, style=self.style)
		answer = answer['input']
		return answer

	def ask_question(self,ask, default=True):
		que = [
			{
				'type': 'confirm',
				'message': ask,
				'name': 'input',
				'default': default,
			}]
		answer = prompt(que, style=self.style)
		return answer['input']

	def get_input(self,ask):
		que = [
				{
					'type': 'input',
					'name': 'input',
					'message': ask,
				}]
		answer = prompt(que, style=self.style)
		return answer['input']

	def pick_one(self, ask, choices):
		que = [
				{
					'type': 'list',
					'name': 'input',
					'message': ask,
					'choices': choices
				}]
		answer = prompt(que, style=self.style)
		return answer['input']

class Snode():
	def __init__(self, dirname, envfile):
		self.dirname = dirname
		self.inquirer = Inquirer()
		self.envfile = envfile
		self.config = dotenv.dotenv_values(self.envfile)

	def get_sudo(self):
		granted = False
		while not granted:
			sudo_pass = self.inquirer.get_input('Type your sudo pass:')
			proc = subprocess.Popen(['sudo', '-S', 'echo', 'VERIFIED'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate(input='{}\n'.format(sudo_pass).encode())
			for response in proc:
				if 'VERIFIED' in response.decode('UTF-8'):
					self.sudo_pass = sudo_pass
					subprocess.Popen(['sudo', '-k'])
					print(f'[bold green]Sudo password verified[/bold green]')
					granted = True
					break
			if not granted:
				subprocess.Popen(['sudo', '-k'])
				print(f'[bold red]Wrong sudo password[/bold red]')

	def comparedisksize(self, app_list, directory_list, req_list):
		if app_list != ['TOTAL']:
			self.dir_cache = {}
		table = Table(box=None)
		table.add_column('',justify='left', style='bold cyan', no_wrap=True)
		table.add_column('Directory',justify='left', style='bold yellow', no_wrap=True)
		table.add_column('Available',justify='left', style='bold yellow', no_wrap=False)
		table.add_column('Required',justify='left', style='bold yellow', no_wrap=False)
		table.add_column('Existing dir',justify='left', style='bold yellow', no_wrap=False)
		table.add_column('',justify='left', style='bold yellow', no_wrap=False)
		table.add_column('Checks',justify='left', no_wrap=False)
		table.add_column('Requirement Calculations',justify='left', style='bold yellow', no_wrap=False)
		for index, app in enumerate(app_list):
			dirr = directory_list[index] if os.path.isdir(directory_list[index]) else str(pathlib.Path(directory_list[index]).parent.absolute())
			hdd = psutil.disk_usage(dirr)
			gb = round(hdd.free / (2**30))
			exists = 0
			found = ''
			try:
				dirs = os.listdir(directory_list[index])
				_app = app
				if app == 'PAYMENT':
					_app = 'eth_pymt_db'
				for i, dir in enumerate(dirs):
					if _app.lower() == dir.lower():
						found = dir
						print(f'Found [bold cyan]{dir}[/bold cyan]')
						proc = subprocess.check_output(f'echo {self.sudo_pass} | sudo -S du -k -d 0 {dirr}/{dir}',stdin=subprocess.PIPE, shell=True)
						data = int(int(proc.decode('UTF-8').split('\t')[0]))
						exists = round(data/float(1<<20),2)
						if dirr in self.dir_cache:
							self.dir_cache[dirr] += exists
						else:
							self.dir_cache[dirr] = exists
						# gb += exists
			except:
				pass
			if app == 'TOTAL':
				if directory_list[index] in self.dir_cache:
					exists = self.dir_cache[directory_list[index]]
			if gb-req_list[index]+exists <=0:
				check = 'WARNING'
				colour = 'red'
			else:
				check = 'PASS'
				colour = 'green'
			table.add_row(app.ljust(8,' '), directory_list[index], f'[{colour}]{"{:.2f}".format(gb)} GB[/{colour}]',f'{req_list[index]} GB',found, f'{exists} GB',f'[bold {colour}]{check}[/bold {colour}]',f'[{colour}]{"{:.2f}".format(gb)}-({req_list[index]}-{exists}) = {"{:.2f}".format(gb-req_list[index]+exists)}[/{colour}] GB')
			if app == 'TOTAL' and check == 'WARNING':
				print(f'[bold red]{"{:.2f}".format(gb-req_list[index]+exists)} GB more are required.\nYou might wanna change a {directory_list[index]} install location.[/bold red]')
		subprocess.Popen(['sudo','-k'])
		print(table)

	def atexit(self):
		if hasattr(self, 'client'):
			self.client.close()
		print("[bold red]Closing...[/bold red]")
		sys.exit(0)

	def checks(self, interval):
		self.client = self.get_client()
		self.check_running_containers(interval)

	def docker_prune(self):
		print('[bold cyan]Checking docker daemon...[/bold cyan]')
		try:
			self.client = docker.from_env()
			print('[bold cyan]Docker found[/bold cyan]')
		except Exception as e:
			self.atexit()
		self.prune_containers()
		self.prune_networks()
		self.prune_volumes()
		self.prune_images()
		self.atexit()

	def get_client(self):
		print('[bold cyan]Checking docker daemon...[/bold cyan]')
		self.check_docker()
		try:
			docker_client = docker.from_env()
			# print('[bold cyan]Docker found[/bold cyan]')
			return docker_client
		except Exception as e:
			print('[bold red]Something happened during Docker checks[/bold red]')
			print("[bold cyan]Consider updating via:[/bold cyan]")
			print("[bold cyan]./exr_env.sh --undocker[/bold cyan]")
			print("[bold cyan]./exr_env.sh --docker[/bold cyan]")
			sys.exit(0)

	def check_docker(self):
		stream = os.popen("which docker")
		output = stream.read()
		if 'docker' not in output:
			print("[bold cyan]Docker not installed[/bold cyan]")
			self.install_docker()
		elif 'docker' in output:
			proc = subprocess.check_output('docker --version',stdin=subprocess.PIPE, shell=True).decode('UTF-8')
			if version.parse(proc.split('version ')[1].split(',')[0]) < version.parse('20.10.13'):
				print("[bold red]Docker Engine version lower than v20.10.13. Please update via:[/bold red]")
				print("[bold cyan]./exr_env.sh --undocker[/bold cyan]")
				print("[bold cyan]./exr_env.sh --docker[/bold cyan]")
				sys.exit(0)				
			else:
				print(f"[bold cyan]Docker Engine version {proc.split('version ')[1].split(',')[0]}[/bold cyan]")
				stream = os.popen("which docker-compose")
				output = stream.read()
				if 'docker-compose' not in output:
					print("[bold cyan]Docker Compose not installed\nPlease install docker, docker-compose or start the daemon to continue...[/bold cyan]")
					sys.exit(0)
				elif 'docker-compose' in output:
					proc = subprocess.check_output('docker-compose --version',stdin=subprocess.PIPE, shell=True).decode('UTF-8')
					if version.parse('.'.join([str(s) for s in proc.split()[-1] if s.isdigit()])) < version.parse("2.3.3"):
						print("[bold red]Docker Compose version lower than v2.3.3. Please update via:[/bold red]")
						print("[bold cyan]docker-compose down[/bold cyan]")
						print("[bold cyan]./exr_env.sh --undocker[/bold cyan]")
						print("[bold cyan]./exr_env.sh --docker[/bold cyan]")
						sys.exit(0)
					else:
						print(f"[bold cyan]docker-compose v{'.'.join([str(s) for s in proc.split()[-1] if s.isdigit()])}[/bold cyan]")

	def install_docker(self):
		answer = self.inquirer.ask_question("Do you want to install docker?")
		if answer ==  True:
			print('[bold cyan]To install docker type:\n./exr_env.sh --docker[/bold cyan]')
			sys.exit(0)
		else:
			print("[bold cyan]Docker daemon error.\nPlease install docker, docker-compose or start the daemon to continue...[/bold cyan]")
			sys.exit(0)

	def check_running_containers(self, interval):
		print('[bold cyan]Checking running containers...[/bold cyan]')
		try:
			containers = self.client.containers.list()
			for c in containers:
				if self.dirname in c.name:
					self.question_containers(interval)
					break
		except Exception as e:
			print(f"Unable to check if [bold cyan]{self.dirname}[/bold cyan] containers are running...\n[bold red]Please stop and remove all {self.dirname} containers to continue[/bold red]")
			sys.exit(0)

	def question_containers(self, interval):
		answer = self.inquirer.ask_question(f'(Will not delete synced blockchain data). Do you want to stop running and remove all {self.dirname} related containers/networks/volumes?')
		if answer == True:
			self.stop_containers(interval)
		else:
			print(f"Current [bold cyan]{self.dirname}[/bold cyan] containers/networks/volumes need to be stopped and removed to continue")
			sys.exit(0)

	def stop_containers(self, interval):
		print(f"Stopping [bold cyan]{self.dirname}[/bold cyan] containers")
		containers = self.client.containers.list()
		for c in containers:
			if self.dirname in c.name:
				print(f"Stopping [bold yellow]{c.name}[/bold yellow]...")
				c.stop(timeout=interval)
				print(f'Waiting to stop [bold yellow]{c.name}[/bold yellow]')
				c.wait()
		self.prune_containers()
		self.prune_networks()
		self.prune_volumes()
		self.prune_images()

	def prune_containers(self):
		# answer = self.inquirer.ask_question('Prune/remove all stopped docker containers? (Y/n)')
		# if answer == True:
		print('[bold cyan]Pruning all stopped docker containers...[/bold cyan]')
		self.client.containers.prune()

	def prune_networks(self):
		# answer = self.inquirer.ask_question('Prune/remove all unused docker networks?  (Y/n)')
		# if answer == True:
		print('[bold cyan]Pruning all docker networks...[/bold cyan]')
		self.client.networks.prune()

	def prune_volumes(self):
		# answer = self.inquirer.ask_question('Prune/remove all unused docker volumes (will not delete synced blockchain data)?  (Y/n)')
		# if answer == True:
		print('[bold cyan]Pruning all docker volumes...[/bold cyan]')
		self.client.volumes.prune()

	def prune_images(self):
		# answer = self.inquirer.ask_question('Prune/remove all unused docker images?  (Y/n)')
		# if answer == True:
		print('[bold cyan]Pruning all docker images...[/bold cyan]')
		self.client.images.prune()

	def externalIP(self):
		try:
			req = requests.get('http://checkip.amazonaws.com')
			req = req.text
			return req[:-1]
		except Exception as e:
			print(e)
			try:
				req = requests.get('http://ifconfig.co')
				req = req.text.split('code')[3].split('>')[1].split('<')[0]
				return req
			except Exception as e:
				print(e)
				return None

	def check_env_var(self, env_var, detail, q1):
		if self.config[env_var]=='':
			if env_var == 'PUBLIC_IP':
				print("Fetching [bold cyan]public IP Address[/bold cyan]...")
				IP = self.externalIP()
				if IP:
					print(f'Found [bold yellow]{env_var}[/bold yellow]=[bold cyan]{IP}[/bold cyan]')
					answer = self.inquirer.get_input(f'Press Enter to confirm {detail} or type a new one:')
					if answer == '':
						answer = IP
					dotenv.set_key(self.envfile, env_var, answer)
					try:
						if answer != socket.gethostbyname(answer):
							print(f'{socket.gethostbyname(answer)} - [bold cyan]{answer}[/bold cyan]')
					except:
						pass
					print(f'Saved [bold yellow]{env_var}[/bold yellow]=[bold cyan]{str(answer)}[/bold cyan]')
				else:
					answer = self.inquirer.get_input(q1)
					dotenv.set_key(self.envfile, env_var, answer)
					try:
						if answer != socket.gethostbyname(answer):
							print(f'{socket.gethostbyname(answer)} - [bold cyan]{answer}[/bold cyan]')
					except:
						pass
					print(f'Saved [bold yellow]{env_var}[/bold yellow]=[bold cyan]{str(answer)}[/bold cyan]')
			else:
				answer = self.inquirer.get_input(q1)
				dotenv.set_key(self.envfile, env_var, answer)
				print(f'Saved [bold yellow]{env_var}[/bold yellow]=[bold cyan]{str(answer)}[/bold cyan]')
		else:
			print(f'Found [bold yellow]{env_var}[/bold yellow]=[bold cyan]{self.config[env_var]}[/bold cyan]')
			answer = self.inquirer.get_input(f'Press Enter to confirm {detail} or type a new one:')	
			if answer == '':
				answer = self.config[env_var]
			dotenv.set_key(self.envfile, env_var, answer)
			print(f'Saved [bold yellow]{env_var}[/bold yellow]=[bold cyan]{str(answer)}[/bold cyan]')

	def env_vars(self):
		env_vars_data = [
		{
		'name': 'PUBLIC_IP',
		'detail': 'external IP address',
		'question': 'What\'s your external/public IP address?',
		},
		{
		'name': 'SN_NAME',
		'detail': 'Servicenode Name',
		'question': 'Set your Servicenode Name:',
		},
		{
		'name': 'SN_KEY',
		'detail': 'Servicenode Private Key',
		'question': 'Set your Servicenode Private Key:',
		},
		{
		'name': 'SN_ADDRESS',
		'detail': 'Servicenode Address',
		'question': 'Set your Servicenode Address:',
		},
		{
		'name': 'RPC_USER',
		'detail': 'Servicenode Username',
		'question': 'Specify a Username for your Servicenode:',
		},
		{
		'name': 'RPC_PASSWORD',
		'detail': 'Servicenode Password',
		'question': 'Specify a Password for your Servicenode:',
		},
		]

		for ev in env_vars_data:
			self.check_env_var(ev['name'],ev['detail'],ev['question'])
	


	def deploy(self):
		proc = subprocess.Popen(['./deploy.sh'], shell=False)
		proc.wait()


