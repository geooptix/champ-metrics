#
# Dockerfile for GeoOptix python2.7 aux metrics calculation
#

# start with an ubuntu base image
FROM ubuntu:16.04

MAINTAINER Keith Steele (keith@sitkatech.com)

# ensure that all the base patches are applied
RUN apt-get update -y

# required tooling
RUN apt-get -y install git
RUN apt-get -y install dos2unix

# install python and pip
RUN apt-get -y install python2.7
RUN apt-get -y install python-pip python-dev build-essential
RUN pip install --upgrade pip
RUN pip install --upgrade virtualenv

# todo: create a virtualenv and install azure-storage into this environment
RUN pip install azure-storage

# create working directory
RUN mkdir -p /usr/src/sitka
WORKDIR /usr/src/sitka

# inject the standard configuration file and the startup script
COPY ./config.ini .
COPY ./champ-metrics.sh .

# clean up line endings to keep everyone happy
RUN dos2unix ./champ-metrics.sh
RUN dos2unix ./config.ini

CMD ./champ-metrics.sh