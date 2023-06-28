#TODO: maybe add functionality to create 1 file per server name to be able to use an llm agent better
import argparse
import json
import os

#options is a list of strings that are the keys of the json file
def keep_only(json_log, options):
    for option in options:
        json_log = json_log[option]
    return json_log

def create_preprocessed_folder(raw_logs_path):
    preprocessed_logs_path = raw_logs_path.replace("raw", "preprocessed")
    os.mkdirs(preprocessed_logs_path)
    return preprocessed_logs_path



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--log_path", help="path to the logs folder")
    args = parser.parse_args()

    #get the list of logs
    logs = os.listdir(args.log_path)
    #create the preprocessed folder
    preprocessed_logs_path = create_preprocessed_folder(args.log_path)

    warning_logs_path = os.path.join(args.log_path, "warning")
    options = ["_source.host.hostname", "_source.message", "_source.@timestamp"]
    #load the json file
    with open(args.json_path) as json_file:
        json_log = json.load(json_file)
    #keep only the message, server and time
    json_log = keep_only(json_log, options)
    #save the json file in the preprocessed folder
    preprocessed_json_path = warning_logs_path.replace("raw", "preprocessed")
    with open(os.path.join(preprocessed_logs_path, preprocessed_json_path), "w") as json_file:
        json.dump(json_log, json_file)

    #chunk json by message

