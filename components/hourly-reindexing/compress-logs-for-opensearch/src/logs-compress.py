#TODO: save the logs to a dataframe and then add them to a chroma db to be able to retrieve them easily
import argparse
import json
import os
import re
from glob import glob
import pandas as pd
import numpy as np
from tqdm import tqdm
from sentence_transformers import SentenceTransformer
from sklearn.cluster import AgglomerativeClustering

#options is a list of strings that are the keys of the json file
def keep_only(json_log, options):
    hits = json_log["hits"]["hits"]
    columns_to_keep = []
    for hit in hits:
        source = hit["_source"]
        keep_only_dict = {}
        for option in options:
            keep_only_dict[option] = source[option]
        columns_to_keep.append(keep_only_dict)
    df = pd.DataFrame(columns_to_keep)
    #fix host column
    try:
        df["host"] = df["host"].apply(lambda x: x['hostname'])
    except:
        pass
    #convert all the columns to string
    df = df.astype(str)
    return df

def create_preprocessed_folder(raw_logs_path):
    preprocessed_logs_path = raw_logs_path.replace("raw", "preprocessed")
    os.makedirs(preprocessed_logs_path, exist_ok=True)
    return preprocessed_logs_path

def get_compressed_logs_df(df, threshold):
    df = df.sort_values(by=['@timestamp'], ascending=False)
    #create embeddings for each message to cluster them on their hostname and message
    sentence_transformer = SentenceTransformer('all-mpnet-base-v2', device='cuda')
    df['embeddings'] = df.apply(lambda x: sentence_transformer.encode(str(x['host']) + str(x['message'])), axis=1)
    #cluster the embeddings
    clustering_model = AgglomerativeClustering(n_clusters=None, distance_threshold=threshold, metric='cosine', linkage='average')
    clustering_model.fit(df['embeddings'].tolist())
    #add cluster column
    df['cluster'] = clustering_model.labels_
    #add sum of cluster column
    df['n_similar_messages'] = df.groupby('cluster')['cluster'].transform('count')
    #add the number of unique hosts in the cluster
    unique_hosts = df.groupby('cluster')['host'].unique()
    df['n_unique_hosts'] = df['cluster'].apply(lambda x: len(unique_hosts[x]))
    #only keep the last message of each cluster
    df = df.drop_duplicates(subset=['cluster'], keep='last').reset_index()
    #TODO: add syslog severity
    #reorder the columns and drop not needed columns
    df = df[['host', 'message','n_unique_hosts', 'n_similar_messages', '@timestamp']]

    return df
def escape_ansi(line):
    line = str(line)
    ansi_escape =re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')
    return ansi_escape.sub('', line)

def save_json_log_to_df(path_to_json_log):
    preprocessed_df_path = path_to_json_log.replace("raw", "preprocessed").replace(".json", ".csv")
    options = ["host", "message", "@timestamp"]
    #load the json file
    with open(path_to_json_log) as json_file:
        json_log = json.load(json_file)
    #keep only the message, server and time
    df_keep_only = keep_only(json_log, options)    
    #convert the timestamp to datetime if empty logs just ignore
    try:
        #convert the timestamp to datetime
        df_keep_only["@timestamp"] = pd.to_datetime(df_keep_only["@timestamp"])
        #sort by timestamp
        df_keep_only = df_keep_only.sort_values(by=['@timestamp'])
        #remove ansi characters
        df_keep_only["message"] = df_keep_only["message"].apply(lambda x: escape_ansi(x))
        #remove \n
        df_keep_only["message"] = df_keep_only["message"].apply(lambda x: x.replace("\n", ""))
    except KeyError:
        df_keep_only.to_csv(preprocessed_df_path, index=False)
        return
    compressed_df = get_compressed_logs_df(df_keep_only, 0.05)
    compressed_df.to_csv(preprocessed_df_path, index=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--log_path",help="path to the folder or subfolder that is inside the/raw/logs folder)")
    parser.add_argument("--day",help="cluster the logs on that day yyyy-mm-dd")
    args = parser.parse_args()

    if args.day != None:
        #check if the folder exists
        preprocessed_day_logs_path = os.path.join("/data/preprocessed/logs/", args.day)
        #if there are logs for each our of the day
        if os.path.isdir(preprocessed_day_logs_path):
            log_levels=["warning", "error", "critical"]
            for log_level in log_levels:
                #get all the logs of the day
                list_of_df_logs = glob(preprocessed_day_logs_path + '/**/*{}.csv'.format(log_level), recursive=True)
                #concatenate all the logs of the day
                df_logs = pd.concat([pd.read_csv(log) for log in list_of_df_logs])
                #compress the logs with a threshold of higher threshold 
                compressed_df = get_compressed_logs_df(df_logs, 0.5)
                #save the compressed logs
                compressed_df.to_csv(os.path.join(preprocessed_day_logs_path, "compressed_{}.csv".format(log_level)), index=False)
        else:
            print("No logs for that day")

    elif args.log_path != None:
        list_of_json_logs = []
        #add to list of json logs all the files inside the folder and subfolders that end with .json
        list_of_json_logs_raw = glob(args.log_path + '/**/*.json', recursive=True)
        list_of_df_logs_preprocessed = glob('/data/preprocessed/logs' + '/**/*.csv', recursive=True)
        #remove the preprocessed logs from the list if already preprocessed
        list_of_json_logs = [log for log in list_of_json_logs_raw if log.replace("raw", "preprocessed").replace(".json", ".csv") not in list_of_df_logs_preprocessed]
        #create the preprocessed folders if they don't exist
        for log in list_of_json_logs_raw:
            preprocessed_folder = log.replace("raw", "preprocessed").replace(log.split("/")[-1], "")
            os.makedirs(preprocessed_folder, exist_ok=True)

        #for each log
        for log_path in tqdm(list_of_json_logs):
            save_json_log_to_df(log_path)