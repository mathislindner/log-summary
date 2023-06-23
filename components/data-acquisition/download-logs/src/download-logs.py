import os
import json
import warnings
import time
from datetime import datetime
from opensearchpy import OpenSearch
import urllib3
import argparse
import kfp.components as comp

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
os.environ['https_proxy']='http://lbproxy.cern.ch:8080' 
os.environ['http_proxy']='http://lbproxy.cern.ch:8080' 
os.environ['no_proxy']="localhost,127.0.0.1,*.cern.ch,*.local,10.0.0.0/8,opensearch.lbdaq.cern.ch"
#TODO: change to only ignore specifically the error: Connecting to https://opensearch.lbdaq.cern.ch:9200 using SSL with verify_certs=False is insecure.
#warnings.simplefilter('ignore')

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

#TODO: returns logs from timeframe in ms
def save_logs(start_time, end_time):
    client = get_client()
    pass

def save_logs_from_today():
    client = get_client()
    syslog_str = 'logstash-syslog-'
    today_str = datetime.today().strftime('%Y.%m.%d')
    outpath ='/data/{}'.format(today_str.replace('.','-'))
    if not os.path.exists(outpath):
        os.mkdir(outpath)
    index_name = syslog_str + today_str

    #get by system log severity
    f = 'syslog_severity'
    #get warnings
    q_names = ['warning', 'crtical', 'error']
    full_queries = []
    #TODO: This might not take all of them
    for q in q_names:
        query = {
            'size': 10000,
            'query':{
                'multi_match': {
                    'query': q,
                    'fields': [f]
                }
            }
        }
        full_queries.append(query)


    for q_name, query in zip(q_names,full_queries):
        response = client.search(
                                body = query,
                                index = index_name
        )
        #json_file = json.dumps(response)
        log_out_path = os.path.join(outpath, q_name + '.json')
        with open(log_out_path,'w') as outfile:
            json.dump(response, outfile)
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s','--start_time')
    #if we do not have the end time, use now as the end time
    parser.add_argument('-e','--end_time')
    #flag for logs from today
    parser.add_argument('-t','--today', action='store_true')
    args = parser.parse_args()
    
    if args.today != None:
        save_logs_from_today()
    else:
        print('missing arguements')
    #elif args.to == None:
    #    args.to = time.now()
    
    #save_logs(args.start_time, args.end_time)

