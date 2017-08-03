#
# Dockerfile for GeoOptix python2.7 aux metrics calculation
#

# start with an ubuntu base image
FROM ubuntu:16.04

MAINTAINER Keith Steele

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

# inject the standard configuration file and the startup script
COPY ./config.ini /
COPY ./champ-metrics.sh /
COPY ./cacert.pem /

# clean up line endings to keep everyone happy
RUN dos2unix ./champ-metrics.sh
RUN dos2unix ./config.ini
RUN dos2unix ./cacert.pem
