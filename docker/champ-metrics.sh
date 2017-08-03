#!/bin/bash

echo 'Starting champ-metrics calculation process'

# initialize a local repo and clone the aux metrics source code
git init
git clone https://github.com/geooptix/champ-metrics.git

# new working directory needs to be where the source from git resides
mv config.ini ./champ-metrics
cd champ-metrics

# fire up python and bootstrap the calculation process
python start.py .\output\champ-metrics.log 3218
