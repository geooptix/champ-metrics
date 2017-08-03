#!/bin/bash

echo 'Starting champ-metrics calculation process'

# establish the working directory for this container
mkdir -p /sitka
cd /sitka

# initialize a local repo and clone the aux metrics projcect
git init
git clone https://github.com/geooptix/champ-metrics.git

# copy the config file that was injected at build time
cd ./champ-metrics
cp /config.ini .

# fire up python and bootstrap the calculation modules
python start.py .\output\champ-metrics.log 3218
