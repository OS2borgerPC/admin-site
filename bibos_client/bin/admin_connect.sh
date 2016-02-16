#!/bin/bash
VERSION=1.0
sudo apt-get update
sudo apt-get upgrade --assume-yes
sudo apt-get install curl --assume-yes
sudo apt-get install python-pip --assume-yes
sudo apt-get install python-dev --assume-yes
sudo pip install netifaces
sudo pip install lockfile
sudo pip install bibos-client
sudo mkdir -p /var/lib/bibos/jobs/
# Set version in configuration
sudo set_bibos_config admin_connect_version $VERSION
sudo register_new_bibos_client.sh
