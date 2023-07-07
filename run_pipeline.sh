#!/bin/bash
export https_proxy=http://lbproxy.cern.ch:8080 ; export http_proxy=http://lbproxy.cern.ch:8080 ; export no_proxy="localhost,127.0.0.1,*.cern.ch,*.local,10.0.0.0/8"
#create volume to share between the dockerfiles
#docker volume create --name temp-vol
TEMP_VOL="/data:/data"
current_dir=$(pwd)
#run data acquisition

    #get the logs
        : '
        cd /root/log-summary/components/data-acquisition/download-logs
        docker build -t log-downloader .
        docker run --network=host -v $TEMP_VOL log-downloader
        '

    #get the alarms
        cd $current_dir/components/data-acquisition/download-alarms
        docker build -t alarm-downloader .
        docker run --network=host -v $TEMP_VOL alarm-downloader


###########################################################################################
#run preprocessing
    #https://python.langchain.com/docs/modules/data_connection/vectorstores/integrations/chroma#basic-example-using-the-docker-container
    #preprocess logs for langchain #TODO: create a database and use compose to run the database and the preprocessor together
        cd $current_dir/components/data-preprocessing/preprocess-logs-for-langchain
        src_path=$(pwd)"/src"
        SRC_VOL=$src_path":/app/src"
        docker build -t logs-preprocessor .
        docker run -it --network=host -v $TEMP_VOL -v $SRC_VOL --device nvidia.com/gpu=all logs-preprocessor /bin/bash

    #preprocess alarms for langchain
        cd $current_dir/components/data-preprocessing/preprocess-alarms-for-langchain
        docker build -t alarm-preprocessor .
        docker run --network=host -v $TEMP_VOL -v$SRC_VOL alarm-preprocessor

#run inference
    #run base inference
        cd $current_dir/components/model-inference/infer-using-huggingface-model
        src_path=$(pwd)"/src"
        SRC_VOL=$src_path":/app/src"
        docker build -t huggingface-inference .
        docker run  -it --network=host -v $TEMP_VOL -v $SRC_VOL --device  nvidia.com/gpu=all huggingface-inference /bin/bash

    #run flask server
        cd $current_dir/components/model-inference/flask-inference
        docker build -t logs-chatbot .
        src_path=$(pwd)"/src"
        SRC_VOL=$src_path":/app/src"
        #docker run  -it --network=host -v $TEMP_VOL -v $SRC_VOL --device  nvidia.com/gpu=all flask-inference /bin/bash
        docker run --network=host -v $TEMP_VOL -v $SRC_VOL --device  nvidia.com/gpu=all flask-inference

    #run chatbot
        cd $current_dir/components/model-inference/logs-chatbot
        docker build -t logs-chatbot .
        src_path=$(pwd)"/src"
        SRC_VOL=$src_path":/app/src"
        docker run  -it --network=host -v $TEMP_VOL -v $SRC_VOL --device  nvidia.com/gpu=all logs-chatbot /bin/bash

    #run local agent pipe
        cd $current_dir/components/model-inference/local-pandas-agent-pipe
        docker build -t local-pandas .
        src_path=$(pwd)"/src"
        SRC_VOL=$src_path":/app/src"
        docker run  -it --network=host -v $TEMP_VOL -v $SRC_VOL --device  nvidia.com/gpu=all local-pandas /bin/bash

    #run LLAMA cpp
        cd $current_dir/components/model-inference/local-pandas-agent-pipe
        docker build -t llama-cpp .
        src_path=$(pwd)"/src"
        SRC_VOL=$src_path":/app/src"
        docker run  -it --network=host -v $TEMP_VOL -v $SRC_VOL --device  nvidia.com/gpu=all llama-cpp /bin/bash