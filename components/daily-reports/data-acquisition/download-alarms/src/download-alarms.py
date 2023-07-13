import os
import argparse
import requests
import json

os.environ['https_proxy']='http://lbproxy.cern.ch:8080' 
os.environ['http_proxy']='http://lbproxy.cern.ch:8080' 
os.environ['no_proxy']="localhost,127.0.0.1,*.cern.ch,*.local,10.0.0.0/8,opensearch.lbdaq.cern.ch"

def save_alarms(start_time, end_time, out_path = "/data/raw/alarms"):
    if not os.path.exists(out_path):
        os.makedirs(out_path)
    result = requests.get("http://10.128.97.82/api/v2/alerts/groups?silenced=false&inhibited=false&active=true")
    split_by_receiver_and_save(out_path, result)
    #save to file
    file_path = os.path.join(out_path, 'all_alarms.json')
    with open(file_path, 'w') as outfile:
        json.dump(result.json(), outfile, indent=4)
        
def split_by_receiver_and_save(out_path, result):
    if not os.path.exists(os.path.join(out_path, 'by_receiver')):
        os.makedirs(os.path.join(out_path, 'by_receiver'))
    for alert in result.json():
        receiver = alert['receiver']['name']
        file_path = os.path.join(out_path, 'by_receiver', receiver + '.json')
        with open(file_path, 'w') as outfile:
            json.dump(alert, outfile, indent=4)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s','--start_time')
    parser.add_argument('-e','--end_time')

    args = parser.parse_args()

    save_alarms(args.start_time, args.end_time)
    