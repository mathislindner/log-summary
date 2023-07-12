#TODO: save the logs to a dataframe and then add them to a chroma db to be able to retrieve them easily
import argparse
import json
import os
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
    df['number_of_similar_messages'] = df.groupby('cluster')['cluster'].transform('count')
    #add the number of unique hosts in the cluster
    unique_hosts = df.groupby('cluster')['host'].unique()
    df['n_unique_hosts'] = df['cluster'].apply(lambda x: len(unique_hosts[x]))
    #only keep the last message of each cluster
    df = df.drop_duplicates(subset=['cluster'], keep='last').reset_index()
    #TODO: add syslog severity
    #reorder the columns and drop not needed columns
    df = df[['host', 'message','n_unique_hosts', 'n_similar_messages', '@timestamp']]

    return df

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
    except KeyError:
        df_keep_only.to_csv(preprocessed_df_path, index=False)
        return
    compressed_df = get_compressed_logs_df(df_keep_only, 0.05)
    compressed_df.to_csv(preprocessed_df_path, index=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--log_path",help="path to the folder or subfolder that is inside the/raw/logs folder)")
    args = parser.parse_args()

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