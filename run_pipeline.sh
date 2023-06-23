#!/bin/bash

#create volume to share between the dockerfiles
#docker volume create --name temp-vol
TEMP_VOL="/data:/data"

#run data acquisition
cd /root/log-summary/components/data-acquisition/download-logs
docker build -t log-downloader .
echo "runnning acquisition..."
docker run --network=host -v $TEMP_VOL log-downloader

#run base inference

#run 