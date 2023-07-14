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
    #preprocessed folder
    preprocessed_logs_folder=$data_path"/preprocessed/logs/"
    #env file path
    env_file=$log_summary_path"/.env"

#set specific variables to the report day
    #second is the day and hour to reindex in the format YYYY-MM-DD one hour before
    day=$(TZ=UTC+0 date -d '-1 day' +'%Y-%m-%d')
    #preprocessed folder for the hour
    preprocessed_logs_folder_day=$preprocessed_logs_folder$day"/"
    #file will be stored in the same folder as the preprocessed but not in an hourly subfolder

#check if the docker images should be rebuild
    if [ "$rebuild" = true ] ; then
        echo "Rebuilding docker images"
        #build all the docker images
        #log-compressor (same as hourly reindexing but different flag)
        cd $log_summary_path/components/hourly-reindexing/compress-logs-for-opensearch
        docker build -t log-compressor .
        #daily-report
        cd $log_summary_path/components/daily-reports/data-export/create-daily-report
        docker build -t daily-report .
        #

    fi


#set volume to share between the dockerfiles
    TEMP_VOL=$data_path":/data"

#run pipeline
    #compress logs and put them in preprocessed folder
    docker run ---network=host -v $TEMP_VOL --tz=Europe/Paris --device nvidia.com/gpu=all log-compressor python3 /app/src/logs-compress.py --day $day
    # (make sure that you have flask-inference running to use the model (or set up another API))
    #create daily report 
    docker run -it --network=host -v $TEMP_VOL --tz=Europe/Paris --env-file $env_file log-summary python3 /app/src/create-daily-report.py --preprocessed_logs $preprocessed_logs_folder_day --day $day
