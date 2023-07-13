import requests
import json
import pandas as pd
import argparse
from glob import glob
import os

def reformat_logs(logs_paths):
    #get the list of logs from df
    logs = []
    for log_path in logs_paths:
        logs.append(pd.read_csv(log_path))
    #concatenate all logs
    df = pd.concat(logs)
    #reformat the logs
    # if messages are identical, the group together and keep last timestamp
    df = df.groupby(['message']).agg({'@timestamp': 'last'}).reset_index()
    df.to_csv("/data/reformated_logs.csv", index=False)

    return 0
    
def get_prompt(df):
    #convert timestamp to datetime
    df['@timestamp'] = pd.to_datetime(df['@timestamp'])
    #only keep hour and minute information to minimize the size of the table for the prompt format was yyyy-mm-dd hh:mm:ss.SSSSSS+00:00
    df['@timestamp'] = df['@timestamp'].dt.strftime('%H:%M')
    #to minimize tokens
    table_to_add = table_to_add.to_json(index=False, orient='split')
    #creates a prompt to create a daily report of the logs as if an system log admin wrote it
    prompt_template = """
    #INSTRUCTIONS:
    You are a system log admin. 
    You are in charge of monitoring the logs of the system.
    You have been tasked to create a daily report of the logs. 
    Each row includes information about the log message and the number of times it appeared in the logs and how many hosts sent the same log message.
    #REPORT
    """
    prompt = "#LOGS \n" + table_to_add + "\n" + prompt_template
    return prompt

def ask_llm(prompt):
    #ask the log language model to generate a report
    url = "http://127.0.0.1:80/query"
    headers = {'Content-Type': 'application/json'}
    data = json.dumps({"userQuery": prompt})
    response = requests.post(url, headers=headers, data=data)
    return response

def post_to_lhcblog(date, text):
    #post the response to the lhcblog
    #read from env variables
    url = os.environ['logbook_url']
    logbook_pwd = os.environ['logbook_pwd']
    headers = {'Content-Type': 'multipart/form-data'}
    data = {
        'CMD': 'Submit',
        'UNM': 'aris-api',
        'UPWD': logbook_pwd,
        'EXP': 'TestLogbook',
        'ENCODING': 'plain',
        'SUBJECT': 'Daily report of the System Logs for {}'.format(date),
        'SYSTEM': 'test',
        'TEXT': text
    }
    response = requests.post(url, headers=headers, data=data)
    return response


if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--report_day', help="day of the report", required=True)
    parser.add_argument('--log_level', help="error, warning", required=True)

    args = parser.parse_args()
    report_day = args.report_day
    log_level = args.log_level
    #if log level not one of the options, exit
    if log_level not in ['error', 'warning']:
        print("log level not one of the options: error, warning")
        exit(1)

    folder_of_day = "/data/preprocessed/logs/{}/".format(report_day)
    #get the compressed logs of the day
    compressed_log = pd.read_csv(os.path.join(folder_of_day, "compressed_{}.csv".format(log_level)))

    prompt_to_send = get_prompt(compressed_log)
    print(prompt_to_send)
    response = ask_llm(prompt_to_send)
    reply = response.json()
    post_to_lhcblog(report_day, reply)
    print(reply)



