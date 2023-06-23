#!/bin/bash

#create volume to share between the dockerfiles
docker volume create temp-vol

#run data acquisition
cd /root/log-summary/components/data-acquisition/download-logs
docker build -t log-downloader
docker run --network=host log-downloader -v temp-vol

#run base inference

#run 