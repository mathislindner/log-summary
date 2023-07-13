#!/bin/bash
#get variables
    #first variable is the path to the log summary folder where the components are (full path)
    log_summary_path=$1
    #second variable is where the data should be stored (full path)
    data_path=$2
    #third variable is if the docker images should be rebuild (true/false)
    rebuild=$3

    #set proxy
    export https_proxy=http://lbproxy.cern.ch:8080 ; export http_proxy=http://lbproxy.cern.ch:8080 ; export no_proxy="localhost,127.0.0.1,*.cern.ch,*.local,10.0.0.0/8"

#set general variables
    #path to raw logs folder
    raw_logs_folder=$data_path"/raw/logs/"
    #preprocessed folder
    preprocessed_logs_folder=$data_path"/preprocessed/logs/"
    #env file path
    env_file=$log_summary_path"/.env"

#set specific variables to the hour
    #second is the day and hour to reindex in the format YYYY-MM-DD one hour before
    day=$(TZ=UTC+0 date -d '-1 hour' +'%Y-%m-%d')
    #third is the hour to reindex in the format HH
    hour=$(TZ=UTC+0 date -d '-1 hour' +'%H')
    #raw logs folder for the hour
    raw_logs_folder_hour=$raw_logs_folder$day"/"$hour"/"
    #preprocessed folder for the hour
    preprocessed_logs_folder_hour=$preprocessed_logs_folder$day"/"$hour"/"

#check if the docker images should be rebuild
    if [ "$rebuild" = true ] ; then
        echo "Rebuilding docker images"
        #build all the docker images
        #log-downloader
        cd $log_summary_path/components/hourly-reindexing/download-logs
        docker build -t log-downloader .
        ##log-compressor
        cd $log_summary_path/components/hourly-reindexing/compress-logs-for-opensearch
        docker build -t log-compressor .
        #log-sender
        cd $log_summary_path/components/hourly-reindexing/send-logs-to-opensearch
        docker build -t log-sender .
    fi


#set volume to share between the dockerfiles
    TEMP_VOL=$data_path":/data"

#run pipeline
    #get the logs last hour 
    docker run --network=host -v $TEMP_VOL --tz=Europe/Paris --env-file $env_file log-downloader python3 /app/src/download-logs.py --day $day --hour $hour
    #compress logs and put them in preprocessed folder
    docker run -it --network=host -v $TEMP_VOL --tz=Europe/Paris --device nvidia.com/gpu=all log-compressor python3 /app/src/logs-compress.py --log_path $raw_logs_folder_hour
    #send logs to opensearch
    preprocessed_logs="/data/preprocessed/logs/2023-07-11"
    docker run -it --network=host -v $TEMP_VOL --tz=Europe/Paris --env-file $env_file log-sender python3 /app/src/send-to-open.py --preprocessed_logs $preprocessed_logs_folder_hour --ignore_sent_logs
