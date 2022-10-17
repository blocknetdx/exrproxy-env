# Enterprise XRouter Environment 
#### Requirements
- `Docker`
- `Docker-Compose`
- `Servicenode Private Key`
- `Servicenode Name`
- `Servicenode Address`
- `Port 80 must be opened on the host`

## env_installer.sh
**Recommended for new Servers/VM/VPS with Ubuntu 20**

If you have never run the  [Enterprise XRouter Environment](https://docs.blocknet.org/resources/glossary/#enterprise-xrouter) _Global Install_ script on your server, or if you have not run it since 1 Oct, 2022, copy/paste these commands to run the  _Global Install_  script:
```
curl -fsSL https://raw.githubusercontent.com/blocknetdx/exrproxy-env-scripts/main/env_installer.sh -o env_installer.sh
chmod +x env_installer.sh
./env_installer.sh --install 
```
(It is required to run this _Global Install_ again after 1 October, 2022 to accommodate a Python dependency broken by a 3rd party.)
If the _Global Install_ Script detects docker/docker-compose is already
installed, it simply won't install new version(s). If it detects
the `~/exrproxy-env` directory already exists, it will update
it. If it detects `~/exrproxy-env` does not already exist, it will
clone it from the Github repository and thereby create it.<br>

Note: The _Global Install_ script only configures the Python
environment for the exrproxy-env located in the user's home
directory. If you have the `exrproxy-env` directory located elsewhere,
you'll will need to switch to using it in the home directory or engage
in some manual tweaking.

__IMPORTANT: This Global Install Script will log you out after it's
finished with phase 1 of the install. This is necessary to update
the user's membership in the *docker* group of Linux and to activate the python
version control system (*pyenv*). Simply log in again after it logs you out,
then issue the following command again to complete phase 2 of the install:__
```
./env_installer.sh --install
```

Then following the steps below.

## Deploy a EXR ENV stack via built-in scripts
* check [Official docs](https://docs.blocknet.org/service-nodes/setup/#deploy-enterprise-xrouter-environment) for more details

### Shell
Generate and deploy a EXR ENV stack
```bash
./exr_env.sh --update --builder "--deploy"
```
Display help message
```bash
./exr_env.sh --help

Enterprise XRouter Proxy Environment
Powered by Blocknet.co

options:
-h | --help       Print this Help.
-u | --update     Update local repo.
-b | --builder    Call builder.py with args.
-v | --version    Print software version and exit.
```
### Python
Generate and deploy a EXR ENV stack
```bash
./builder.py --deploy
```
Display help message
```
./builder.py --help
usage: builder.py [-h] [--nochecks] [--noenv] [--deploy] [--prune]
                  [--source SOURCE] [--yaml YAML] [--interval INTERVAL]
                  [--branchpath BRANCHPATH] [--prunecache] [--subnet SUBNET]

optional arguments:
  -h, --help            show this help message and exit
  --nochecks            Don't check docker requirements
  --noenv               Don't check if .env file exists (only for advanced
                        users)
  --deploy              Autodeploy stack
  --prune               Prune docker
  --source SOURCE       Source file
  --yaml YAML           Custom input yaml
  --interval INTERVAL   Docker stopping interval till sends SIGKILL signal; default 30s
  --branchpath BRANCHPATH
  --xquerytag TAG 
  --prunecache          Reinit .known_hosts, .known_volumes, .env and .cache
                        files
  --subnet SUBNET       Subnet to configure docker-compose network 
```


## Create Project

See [Request Project API](https://api.blocknet.org/#request_project)

## Checking stack

There are three python scripts to check API in `auto_test` directory:

- exr_methods.py - RPC calls to exr
- xrouter_methods.py - RPC calls to xrouter
- snode_methods.py - RPC calls to snode 

RPC methods are stored in json files. You are free to add/remove them. 

_More details in auto_test/README.md_

Examples: 

Retrieving the current block height of the longest chain for the specified blockchain.
_Make sure your xrouter config supports specified blockchain._ 
```bash 
python3 xrouter_methods.py LTC http://127.0.0.1 xrouter_methods.json 
----------------------------------------
Method xrGetBlockCount HTTP status code 200
1966098

python3 xrouter_methods.py BTC http://127.0.0.1 xrouter_methods.json 
----------------------------------------
Method xrGetBlockCount HTTP status code 200
2034177

python3 xrouter_methods.py BTC http://127.0.0.1 xrouter_methods.json 
----------------------------------------
Method xrGetBlockCount HTTP status code 200
2034177

python3 exr_methods.py project --api-key N8Zk0-hBRqD81dmBDEQP5qUpf9-XKz5eVPcstPkr8C0 --project-id 6228e1ed-1c78-40ca-9813-421d0fdfbfcf  http://127.0.0.1 exr_methods.json
---------------------------------------
Method eth_blockNumber HTTP status code 200
0xa2028a
---------------------------------------
Method eth_chainId HTTP status code 200
0x3
```
