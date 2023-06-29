#TODO: maybe add functionality to create 1 file per server name to be able to use an llm agent better
import argparse
import json
import os
import pandas as pd

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
    print(df.head())
    return df

def create_preprocessed_folder(raw_logs_path):
    preprocessed_logs_path = raw_logs_path.replace("raw", "preprocessed")
    os.makedirs(preprocessed_logs_path, exist_ok=True)
    return preprocessed_logs_path

def save_json_log_to_df(path_to_json_log):
    options = ["host", "message", "@timestamp"]
    #load the json file
    with open(path_to_json_log) as json_file:
        json_log = json.load(json_file)
    #keep only the message, server and time
    df_keep_only = keep_only(json_log, options)
    #save the json file in the preprocessed folder
    preprocessed_df_path = path_to_json_log.replace("raw", "preprocessed").replace(".json", ".csv")
    df_keep_only.to_csv(preprocessed_df_path, index=False)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--log_path", help="path to the logs folder")
    args = parser.parse_args()

    #get the list of logs
    logs = os.listdir(args.log_path)
    #create the preprocessed folder
    preprocessed_logs_path = create_preprocessed_folder(args.log_path)

    #for each log
    for log in logs:
        #save the json log to a dataframe
        json_log_path = os.path.join(args.log_path, log)
        save_json_log_to_df(json_log_path)
        #save the dataframe in the preprocessed folder


    
    #chunk json by message

