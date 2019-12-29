#!/bin/bash

sudo apt-get install apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
curl -sSL https://get.docker.com | sh
sudo usermod -aG docker pi
sudo apt-get install libffi-dev libssl-dev
sudo apt-get install -y python python-pip
sudo pip install docker-compose
mkdir -p /srv/homeassistant
curl -sL https://raw.githubusercontent.com/home-assistant/hassio-installer/master/hassio_install.sh > /tmp/hassio_install.sh
sudo bash /tmp/hassio_install.sh -m raspberrypi4 -d /srv/homeassistant
