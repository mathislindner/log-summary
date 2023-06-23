#!/bin/bash

#create volume to share between the dockerfiles
#docker volume create --name temp-vol
TEMP_VOL="/data:/data"

#run data acquisition

    #get the logs
        : '
        cd /root/log-summary/components/data-acquisition/download-logs
        docker build -t log-downloader .
        docker run --network=host -v $TEMP_VOL log-downloader
        '

    #get the alarms
        cd /root/log-summary/components/data-acquisition/download-alarms
        docker build -t alarm-downloader .
        docker run --network=host -v $TEMP_VOL alarm-downloader


###########################################################################################
#run preprocessing
    #preprocess alarms for langchain
        cd /root/log-summary/components/data-preprocessing/preprocess-alarms-for-langchain
        docker build -t alarm-preprocessor .
        docker run --network=host -v $TEMP_VOL alarm-preprocessor

#run base inference

#run 