#!/usr/bin/env python3

import psycopg2 as db
import subprocess
import docker
from datetime import datetime
from rich.table import Table
from rich import print
import argparse
import os
import requests
from dateutil.parser import parse

def get_payment_db_ip():
	inspect_out = subprocess.check_output(f'docker inspect exrproxy-env-payment_db-1',stdin=subprocess.PIPE, shell=True) 
	lines = inspect_out.decode("UTF-8").split("\n")
	return [line for line in lines if "IPv4Address" in line][0].split('"')[3]

def request_project():
	headers = {'Content-Type':'application/json'}
	payload = '{"jsonrpc":"2.0","method":"request_project","params": [], "id":1}'
	response = requests.post(url="http://127.0.0.1/xrs/projects",headers=headers,data=payload)
	if response.status_code == 200:
		if 'result' in response.json().keys():
			project_id = response.json()['result']['project_id']
			return project_id
		else:
			print('[bold red]Error occured requesting new project[/bold red]')
			print(response.json())
			return False
	else:
		print('[bold red]Error occured requesting new project[/bold red]')
		print(response.json())
		return False

def is_date(string, fuzzy=False):
	try:
		return parse(string, fuzzy=fuzzy)
	except ValueError:
		return False

def exec_psql(cmd, host, database, user, password):
	try:
		conn = db.connect(host=host, database=database, user=user, password=password)
		conn.autocommit = True
		cursor = conn.cursor()
		cursor.execute(cmd)
		op,_=cmd.lower().split(maxsplit=1)
		if op == 'select':
			results = cursor.fetchall()
		else:
			results = f'{cursor.rowcount} row(s) affected'
		conn.close()
		return results
	except Exception as e:
		# print(f'[bold red]FAILED {cmd}\n{e}[/bold red]')
		return False

def column_names(table, host, database, user, password):
	result = exec_psql(f"select column_name from information_schema.columns where table_name = '{table}' order by ordinal_position", host, database, user, password)
	if result != False:
		return [x[0] for x in result]
	else:
		return result

def all_data(table, project, host, database, user, password):
	cmd = f"select * from {table}"
	if project:
		if table == 'project':
			cmd += f" where name='{project}'"
		elif table == 'payment':
			cmd += f" where project='{project}'"

	result = exec_psql(cmd, host, database, user, password)
	if result != False:
		data = []
		for row in result:
			r = []
			for item in row:
				if isinstance(item, datetime):
					r.append(item.strftime("%m/%d/%Y, %H:%M:%S"))
				else:
					r.append(str(item))
			data.append(r)
		return data
	else:
		return result

def get_table(table, project, id, host, database, user, password):
	data = all_data(table, project, host, database, user, password)
	headers = column_names(table, host, database, user, password)
	if headers != False and data != False:
		if id>0 and len(data)>=id:
			data = [data.pop(id-1)]
		data.insert(0,headers)
		return data
	else:
		return False

def render_table(table, project, id, host, database, user, password):
	result = get_table(table, project, id, host, database, user, password)
	if result:
		if id==0 and project==False:
			table = Table(title=table.capitalize(),title_justify='left',title_style='bold cyan', box=None, expand=True)
			for header in result[0]:
				table.add_column(header, justify='left', style='yellow',no_wrap=True)
			for data in result[1::]:
				table.add_row(*data)
			print()
			print(table)
			print()
		elif id!=0 or project!=False:
			table = Table(title=table.capitalize(),title_justify='left',title_style='bold cyan', box=None, expand=True)
			table.add_column(justify='left', style='bold white',no_wrap=True)
			table.add_column(justify='left', style='yellow',no_wrap=True)
			for i in range(len(result[0])):
				data = [result[0][i],result[1][i]]
				table.add_row(*data)
			print()
			print(table)
			print()

def help(host_ip):
	print(f'[bold red]{"-"*20}[/bold red]')
	table = Table(box=None)
	table.add_column('Argument',justify='left', style='green', no_wrap=False)
	table.add_column('Help',justify='left', style='yellow', no_wrap=False)
	table.add_column('Defaults',justify='left', style='bold cyan', no_wrap=False)
	data = [
		['--help | -h', 'Print help'],
		['--host', "IP address of [bold cyan]payment_db[/bold cyan] container", host_ip],
		['--username | -u', 'Username for [bold cyan]payment_db[/bold cyan]', 'ethproxy'],
		['--password | -p', 'Password for [bold cyan]payment_db[/bold cyan]', 'password'],
		['--db | -d', 'Database from [bold cyan]payment_db[/bold cyan]', 'eth'],
		['--all', 'Show all projects and their details'],
		['--balances', 'Show all payments and their details'],
		['--id', 'Select line from table to show details for'],
		['--project', 'Show details for project'],
		['--date', 'Format: [bold yellow]Y/M/D or M/D/Y[/bold yellow]. Change expiration date of a project in the [bold yellow]Project[/bold yellow] table'],
		['--apicount', 'Change apicount number of a project in the [bold yellow]Project[/bold yellow] table'],
		['--archive', 'Toggle the archive boolean of a project in [bold yellow]Project[/bold yellow] table'],
		['--active', 'Toggle the active boolean of a project in [bold yellow]Project[/bold yellow] table '],
		['--cmd', 'Send SQL to [bold cyan]payment_db[/bold cyan]'],
		['--new', 'Request new Project ID and Api-Key']
	]
	for d in data:
		table.add_row(*d)

	print(table)
	print()
	print(f'[bold red]{"-"*20}[/bold red]')

	table = Table(title='Arguments Combinations', title_justify='left', title_style='bold cyan', box=None)
	table.add_column('Arguments',justify='left', style='green', no_wrap=False)
	table.add_column('Details',justify='left', style='yellow', no_wrap=False)
	table.add_column('Defaults',justify='left', style='bold cyan', no_wrap=False)
	data = [
		['--help | -h','Print help'],
		['--host [bold yellow]IP[/bold yellow]', "IP address of [bold cyan]payment_db[/bold cyan] container", host_ip],
		['--username [bold yellow]USERNAME[/bold yellow]', 'Username for [bold cyan]payment_db[/bold cyan]', 'ethproxy'],
		['--password [bold yellow]PASSWORD[/bold yellow]', 'Password for [bold cyan]payment_db[/bold cyan]', 'password'],
		['--db [bold yellow]DB[/bold yellow]', 'Database from [bold cyan]payment_db[/bold cyan]', 'eth'],
		['--all', 'Show all projects and their details'],
		['--balances','Show all payments and their details'],
		['--project [bold yellow]f8cc8cfc-e34a-4c66-86ae-2fef9d29da64[/bold yellow]', 'Show details for [bold yellow]f8cc8cfc-e34a-4c66-86ae-2fef9d29da64[/bold yellow]'],
		['--all --id [bold yellow]1[/bold yellow]','Show line [bold yellow]1[/bold yellow] of [bold yellow]Project[/bold yellow] table'],
		['--balances --id [bold yellow]1[/bold yellow]','Show line [bold yellow]1[/bold yellow] of [bold yellow]Payment[/bold yellow] table'],
		['--project [bold yellow]f8cc8cfc-e34a-4c66-86ae-2fef9d29da64[/bold yellow] --date [bold yellow]2022/4/8[/bold yellow]', 'Change [bold yellow]f8cc8cfc-e34a-4c66-86ae-2fef9d29da64[/bold yellow] expiration date to [bold yellow]2022/4/8[/bold yellow]'],
		['--project [bold yellow]f8cc8cfc-e34a-4c66-86ae-2fef9d29da64[/bold yellow] --apicount [bold yellow]100[/bold yellow]', 'Change [bold yellow]f8cc8cfc-e34a-4c66-86ae-2fef9d29da64[/bold yellow] api count to [bold yellow]100[/bold yellow]'],
		['--project [bold yellow]f8cc8cfc-e34a-4c66-86ae-2fef9d29da64[/bold yellow] --archive', 'Toggle [bold yellow]f8cc8cfc-e34a-4c66-86ae-2fef9d29da64[/bold yellow] [bold yellow]ARCHIVE MODE BOOLEAN[/bold yellow]'],
		['--project [bold yellow]f8cc8cfc-e34a-4c66-86ae-2fef9d29da64[/bold yellow] --active', 'Toggle [bold yellow]f8cc8cfc-e34a-4c66-86ae-2fef9d29da64[/bold yellow] [bold yellow]ACTIVE BOOLEAN[/bold yellow]'],
		['--cmd [bold yellow]"select * from project"[/bold yellow]', 'Execute [bold yellow]"select * from project"[/bold yellow]'],
		['--new', 'Request new Project ID and Api-Key']
	]
	for d in data:
		table.add_row(*d)

	print(table)

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='CLI simple interface for managing EXR ENV projects', add_help=False)
	parser.add_argument('--help','-h', action='store_true')
	parser.add_argument('--host', default=get_payment_db_ip())
	parser.add_argument('--username','-u', default='ethproxy')
	parser.add_argument('--password','-p', default='password')
	parser.add_argument('--db','-d', default='eth')
	parser.add_argument('--all', action='store_true')
	parser.add_argument('--balances', action='store_true')
	parser.add_argument('--id', default=0, type=int)
	parser.add_argument('--project', default=False)
	parser.add_argument('--date', default=False)
	parser.add_argument('--apicount', default=False)
	parser.add_argument('--archive', action='store_true')
	parser.add_argument('--active', action='store_true')
	parser.add_argument('--cmd', default=False, type=str)
	parser.add_argument('--new', action='store_true')

	args = parser.parse_args()
	HELP = args.help
	HOST = args.host
	USERNAME = args.username
	PASSWORD = args.password
	DB = args.db
	ALL = args.all
	BAL = args.balances
	ID = args.id
	PROJECT = args.project
	DATE = args.date
	APICOUNT = args.apicount
	ARCHIVE = args.archive
	ACTIVE = args.active
	CMD = args.cmd
	NEW = args.new

	print('[bold cyan]Enterprise[/bold cyan] [bold green]XRouter[/bold green] [bold cyan]Environment[/bold cyan] [bold yellow]Projects[/bold yellow] [bold magenta]CLI[/bold magenta]')
	if ALL and not ARCHIVE and not ACTIVE and not APICOUNT and not DATE and not CMD:
		render_table('project', PROJECT, ID, HOST, DB, USERNAME, PASSWORD)
	elif BAL and not ARCHIVE and not ACTIVE and not APICOUNT and not DATE and not CMD:
		render_table('payment', PROJECT, ID, HOST, DB, USERNAME, PASSWORD)
	elif PROJECT and not ARCHIVE and not ACTIVE and not APICOUNT and not DATE and not CMD:
		render_table('project', PROJECT, ID, HOST, DB, USERNAME, PASSWORD)
		render_table('payment', PROJECT, ID, HOST, DB, USERNAME, PASSWORD)
	elif PROJECT and ARCHIVE or ACTIVE or APICOUNT or DATE and not CMD:
		if DATE:
			if is_date(DATE):
				string = is_date(DATE).strftime("%Y-%m-%d")
				exec_psql(f"update project set expires = COALESCE(expires, '{string}'::date) where name='{PROJECT}'", HOST, DB, USERNAME, PASSWORD)
				exec_psql(f"update project set expires='{string}'::date + expires::time where name='{PROJECT}'", HOST, DB, USERNAME, PASSWORD)
		if APICOUNT:
			exec_psql(f"update project set api_token_count='{APICOUNT}' where name='{PROJECT}'", HOST, DB, USERNAME, PASSWORD)
		if ARCHIVE:
			exec_psql(f"update project set archive_mode = COALESCE(archive_mode, False) where name='{PROJECT}'", HOST, DB, USERNAME, PASSWORD)
			exec_psql(f"update project set archive_mode = NOT archive_mode where name='{PROJECT}'", HOST, DB, USERNAME, PASSWORD)
		if ACTIVE:
			exec_psql(f"update project set active = NOT active where name='{PROJECT}'", HOST, DB, USERNAME, PASSWORD)
		render_table('project', PROJECT, ID, HOST, DB, USERNAME, PASSWORD)
	elif CMD:
		result = exec_psql(CMD, HOST, DB, USERNAME, PASSWORD)
		if result:
			print(result)
		else:
			print(f'[bold red]Error occured when executing:\n{CMD}[/bold red]')
	elif NEW:
		newproject = request_project()
		if newproject:
			render_table('project', newproject, ID, HOST, DB, USERNAME, PASSWORD)
			render_table('payment', newproject, ID, HOST, DB, USERNAME, PASSWORD)
	else:
		help(HOST)
