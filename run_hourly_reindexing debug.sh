#!/bin/bash
#first variable is the path to the log summary folder
log_summary_path=$1
export https_proxy=http://lbproxy.cern.ch:8080 ; export http_proxy=http://lbproxy.cern.ch:8080 ; export no_proxy="localhost,127.0.0.1,*.cern.ch,*.local,10.0.0.0/8"
#create volume to share between the dockerfiles
TEMP_VOL="/data:/data"

#get the logs last hour 
    cd $log_summary_path/components/data-acquisition/download-logs
    docker build -t log-downloader .
    TEMP_VOL="/data:/data"
    cwd=$(pwd)
    SRC_VOL=$cwd"/src:/app/src"
    #docker run --network=host -v $TEMP_VOL --tz=Europe/Paris log-downloader
    #debug
    docker run -it --network=host -v $TEMP_VOL --tz=Europe/Paris -v $SRC_VOL  log-downloader /bin/bash

#compress logs and put them in preprocessed folder
    cd $log_summary_path/components/data-preprocessing/compress-logs-for-opensearch
    docker build -t log-compressor .
    #docker run --network=host -v $TEMP_VOL --tz=Europe/Paris log-compressor
    #debug
    TEMP_VOL="/data:/data"
    cwd=$(pwd)
    SRC_VOL=$cwd"/src:/app/src"
    docker run -it --network=host -v $TEMP_VOL --tz=Europe/Paris -v $SRC_VOL nvidia.com/gpu=all  log-compressor /bin/bash


#send logs to opensearch
    cd $log_summary_path/components/data-export/send-logs-to-opensearch
    docker build -t log-sender .
    #docker run --network=host -v --tz=Europe/Paris $TEMP_VOL log-sender
    #debug
    TEMP_VOL="/data:/data"
    cwd=$(pwd)
    SRC_VOL=$cwd"/src:/app/src"
    docker run -it --network=host -v $TEMP_VOL --tz=Europe/Paris -v $SRC_VOL  log-sender /bin/bash
