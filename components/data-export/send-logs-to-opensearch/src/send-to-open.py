import os
from glob import glob
import json
from datetime import datetime, timedelta, timezone
import time
from tqdm import tqdm
import pandas as pd
from opensearchpy import OpenSearch
import urllib3
import argparse

def load_config():
    f = open('src/config.json')
    config = json.load(f)
    return config

def get_client():
    config = load_config()
    # Create the client instance
    client = OpenSearch(
        hosts = [{'host': config['HOST'], 'port':config['PORT']}],
        http_auth = (config['USERNAME'],config['PASSWORD']),
        use_ssl = True,
        ca_certs=False,
        verify_certs=False        
    )
    # Successful response!
    client.info()
    return client
def get_index_name(log_path):
    base_name = "compressed-logstash-syslog-"
    #get the date from the log path
    date = log_path.split('/')[-3]
    index_name = base_name + date
    return index_name

def send_log_to_opensearch(log_path):
    client = get_client()
    log_df = pd.read_csv(log_path, sep='\t')
    index_name = get_index_name(log_path)
    print("sending log:{} to index:{}".format(log_path, index_name))
    
    #create the index if it does not exist
    if not client.indices.exists(index_name):
        client.indices.create(index_name)
    #send the log to opensearch
    if log_df.empty:
        return True
    try:
        body = log_df.to_dict(orient='records')
        client.bulk(body, index=index_name)
        return True
    except Exception as e:
        print("Error sending log: {} to opensearch".format(log_path))
        print(e)
    return False

def is_empty_df(fpath):  
    try:
        df = pd.read_csv(fpath, sep='\t')
        return df.empty
    except Exception as e:
        return True

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p','--preprocessed_logs', help="path to the preprocessed logs folder", required=True)
    args = parser.parse_args()

    #create file to save the logs that were sent in the /data/sent-opensearch-logs.txt
    sent_logs_path = os.path.join('/data','preprocessed', "sent-opensearch-logs.txt")
    if not os.path.exists(sent_logs_path):
        with open(sent_logs_path, 'w') as f:
            f.write("")
    #get the list of preprocessed logs and from subfolders
    preprocessed_logs = glob(os.path.join(args.preprocessed_logs, '**', '*.csv'), recursive=True)
    #get the list of logs that were already sent
    with open(sent_logs_path, 'r') as f:
        sent_logs = f.readlines()
    sent_logs = [log.replace("\n", "") for log in sent_logs]
    #add to sent logs if the log file is empty
    for log in preprocessed_logs:
        if is_empty_df(log) and log not in sent_logs:
            sent_logs.append(log)
            with open(sent_logs_path, 'a') as f:
                f.write(log+"\n")
    #get the list of logs that were not sent
    logs_to_send = [log for log in preprocessed_logs if log not in sent_logs]
    print("sending {} logs to opensearch".format(len(logs_to_send)))

    for log in tqdm(logs_to_send):
        success = False
        tries = 0
        while not success or tries < 3:
            success = send_log_to_opensearch(log)
            tries += 1
            if success:
                with open(sent_logs_path, 'a') as f:
                    f.write(log+"\n")
                break
            else:
                time.sleep(5)
        if not success:
            print("failed to send log: ", log)


