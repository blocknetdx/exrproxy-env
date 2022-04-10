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
		results = cursor.fetchall()
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
		if id!=0:
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

def help():
	print(f'[bold red]{"-"*20}[/bold red]')
	table = Table(box=None)
	table.add_column('Argument',justify='left', style='green', no_wrap=False)
	table.add_column('Help',justify='left', style='yellow', no_wrap=False)
	table.add_column('Defaults',justify='left', style='bold cyan', no_wrap=False)
	data = [
		['--help | -h', 'Print help'],
		['--host', "IP address of [bold cyan]payment_db[/bold cyan] container"],
		['--username | -u', 'Username for [bold cyan]eth_pay_db[/bold cyan]', 'ethproxy'],
		['--password | -p', 'Password for [bold cyan]eth_pay_db[/bold cyan]', 'password'],
		['--db | -d', 'Database from [bold cyan]eth_pay_db[/bold cyan]', 'eth'],
		['--all', 'Show all projects and their details'],
		['--balances', 'Show all payments and their details'],
		['--id', 'Select line from table to show details for'],
		['--project', 'Show details for project'],
		['--date', 'Format: [bold yellow]Y/M/D or M/D/Y[/bold yellow]. Change expiration date of a project in the [bold yellow]Project[/bold yellow] table'],
		['--apicount', 'Change apicount number of a project in the [bold yellow]Project[/bold yellow] table'],
		['--archive', 'Change the archive boolean of a project in a [bold yellow]Project[/bold yellow] table'],
		['--active', 'Change the active boolean of a project in a [bold yellow]Project[/bold yellow] table '],
		['--cmd', 'Send command to [bold cyan]eth_pay_db[/bold cyan]'],
		['--new', 'Request new Project ID and Api-Key']
	]
	for d in data:
		table.add_row(*d)

	print(table)
	print()
	print("[red]Use this command to get [bold cyan]payment_db[/bold cyan] IP address:[/red]")
	print("""[red]docker inspect $(docker ps | grep payment_db | awk '{print $1}') | sed -nE '/"IPv4Address":[ \t]"[[:digit:]]/{s/[ \t]*"IPv4Address":[ \t]+"([0-9.]+)"/\1/p;}'[/red]""")
	print()
	print(f'[bold red]{"-"*20}[/bold red]')

	table = Table(title='Arguments Combinations', title_justify='left', title_style='bold cyan', box=None)
	table.add_column('Arguments',justify='left', style='green', no_wrap=False)
	table.add_column('Details',justify='left', style='yellow', no_wrap=False)
	table.add_column('Defaults',justify='left', style='bold cyan', no_wrap=False)
	data = [
		['--help | -h','Print help'],
		['--host [bold yellow]IP[/bold yellow]', "IP address of [bold cyan]payment_db[/bold cyan] container"],
		['--username [bold yellow]USERNAME[/bold yellow]', 'Username for [bold cyan]eth_pay_db[/bold cyan]', 'ethproxy'],
		['--password [bold yellow]PASSWORD[/bold yellow]', 'Password for [bold cyan]eth_pay_db[/bold cyan]', 'password'],
		['--db [bold yellow]DB[/bold yellow]', 'Database from [bold cyan]eth_pay_db[/bold cyan]', 'eth'],
		['--all', 'Show all projects and their details'],
		['--balances','Show all payments and their details'],
		['--project [bold yellow]f8cc8cfc-e34a-4c66-86ae-2fef9d29da64[/bold yellow]', 'Show details for [bold yellow]f8cc8cfc-e34a-4c66-86ae-2fef9d29da64[/bold yellow]'],
		['--all --id [bold yellow]1[/bold yellow]','Show line [bold yellow]1[/bold yellow] of [bold yellow]Project[/bold yellow] table'],
		['--balances --id [bold yellow]1[/bold yellow]','Show line [bold yellow]1[/bold yellow] of [bold yellow]Payment[/bold yellow] table'],
		['--project [bold yellow]f8cc8cfc-e34a-4c66-86ae-2fef9d29da64[/bold yellow] --date [bold yellow]2022/4/8[/bold yellow]', 'Change [bold yellow]f8cc8cfc-e34a-4c66-86ae-2fef9d29da64[/bold yellow] expiration date to [bold yellow]2022/4/8[/bold yellow]'],
		['--project [bold yellow]f8cc8cfc-e34a-4c66-86ae-2fef9d29da64[/bold yellow] --apicount [bold yellow]100[/bold yellow]', 'Change [bold yellow]f8cc8cfc-e34a-4c66-86ae-2fef9d29da64[/bold yellow] api count to [bold yellow]100[/bold yellow]'],
		['--project [bold yellow]f8cc8cfc-e34a-4c66-86ae-2fef9d29da64[/bold yellow] --archive', 'Change [bold yellow]f8cc8cfc-e34a-4c66-86ae-2fef9d29da64[/bold yellow] archive mode boolean to [bold yellow]NOT ARCHIVE MODE BOOLEAN[/bold yellow]'],
		['--project [bold yellow]f8cc8cfc-e34a-4c66-86ae-2fef9d29da64[/bold yellow] --active', 'Change [bold yellow]f8cc8cfc-e34a-4c66-86ae-2fef9d29da64[/bold yellow] active boolean to [bold yellow]NOT ACTIVE BOOLEAN[/bold yellow]'],
		['--cmd [bold yellow]"select * from project"[/bold yellow]', 'Execute [bold yellow]"select * from project"[/bold yellow]'],
		['--new', 'Request new Project ID and Api-Key']
	]
	for d in data:
		table.add_row(*d)

	print(table)

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='CLI simple interface for managing EXR ENV projects', add_help=False)
	parser.add_argument('--help','-h', action='store_true')
	parser.add_argument('--host', default=False)
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

	if HOST:
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
					exec_psql(f"update project set expires='{string}'::date + expires::time where name='{PROJECT}'", HOST, DB, USERNAME, PASSWORD)
			if APICOUNT:
				exec_psql(f"update project set api_token_count='{APICOUNT}' where name='{PROJECT}'", HOST, DB, USERNAME, PASSWORD)
			if ARCHIVE:
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
			help()
	elif HELP:
		help()
	else:
		print('[bold red]--host is missing[/bold red]')
		help()
