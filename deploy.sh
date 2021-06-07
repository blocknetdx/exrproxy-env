#!/bin/bash

DOCKER_COMPOSE_VERSION="1.26.2"

# Install Docker
function installdocker() {
    sudo apt-get update -y
    sudo apt-get install -y \
        apt-transport-https \
        ca-certificates \
        curl \
        gnupg-agent \
        software-properties-common

    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add - 
    sudo apt-key fingerprint 0EBFCD88
    sudo add-apt-repository -y \
        "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
        $(lsb_release -cs) \
        stable"
    sudo apt-get -y update
    sudo apt-get -y install docker-ce docker-ce-cli containerd.io

    sudo curl -L "https://github.com/docker/compose/releases/download/${DOCKER_COMPOSE_VERSION}/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
}

read -p 'Install Docker? [y/n] ' inst_docker
if [ $inst_docker = "y" ]; then
   installdocker
else
  echo "Not installing Docker..."
fi

read -p 'Your Public IP Address: ' PUBLIC_IP

# GETH EXTERNAL
if [ "$1" = "gethexternal" ]; then
  read -p 'GETH HOST: ' GETH_HOST
fi

read -p 'Servicenode Name: ' SN_NAME
read -sp 'Servicenode Private Key: ' SN_KEY
echo
read -p 'Servicenode Address: ' SN_ADDRESS

echo "Please specify an user and password for the new servicenode"
read -p 'RPC Username: ' RPC_USER
read -sp 'RPC Password: ' RPC_PASSWORD
echo

if [ "$1" = "dev" ]; then
  echo "Development mode"
  PUBLIC_IP=$PUBLIC_IP SN_NAME=$SN_NAME SN_KEY=$SN_KEY SN_ADDRESS=$SN_ADDRESS RPC_USER=$RPC_USER RPC_PASSWORD=$RPC_PASSWORD docker-compose -f "docker-compose-dev.yml" up -d --build
elif [ "$1" = "gethexternal" ]; then
  PUBLIC_IP=$PUBLIC_IP SN_NAME=$SN_NAME SN_KEY=$SN_KEY SN_ADDRESS=$SN_ADDRESS RPC_USER=$RPC_USER RPC_PASSWORD=$RPC_PASSWORD GETH_HOST=$GETH_HOST docker-compose -f "docker-compose-geth-external.yml" up -d --build
else
  PUBLIC_IP=$PUBLIC_IP SN_NAME=$SN_NAME SN_KEY=$SN_KEY SN_ADDRESS=$SN_ADDRESS RPC_USER=$RPC_USER RPC_PASSWORD=$RPC_PASSWORD docker-compose -f "docker-compose.yml" up -d --build
fi
