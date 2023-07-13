import os
import json
from datetime import datetime, timedelta, timezone
import time
from opensearchpy import OpenSearch
import urllib3
import argparse

#disable all the warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
#set the proxy
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

#FIXME: does not take care of different log indices on different days
def download_logs_in_time_frame(start_time, end_time, last_hour=False):
    #add time zone
    day_of_last_hour = start_time.strftime('%Y.%m.%d')
    if last_hour == True:
        outpath ='/data/raw/logs/{}/{}'.format(day_of_last_hour.replace('.','-'), start_time.strftime('%H'))
    #else the range will be the folder name
    else:
        outpath ='/data/raw/logs/ownquery/{}to{}'.format(start_time.strftime('%Y-%m-%dT%H:%M:%S'), end_time.strftime('%Y-%m-%dT%H:%M:%S'))
    if not os.path.exists(outpath):
        os.makedirs(outpath)
    index_name = 'logstash-syslog-' + day_of_last_hour
    q_names = ['warning', 'crtical', 'error']
    full_queries = []
    #doing it in 3 queries because of the 10k limit and so we can easily save them separately
    print('Downloading logs from {} to {}. From index: {}'.format(start_time, end_time, index_name))
    for q in q_names:
        query = {
            'size': 10000,
            'query':{
                "bool": {
                    'must':[{
                        'multi_match':{
                            'query': q,
                            'fields': ['syslog_severity']
                        }
                        },
                        {
                        'range':{
                            '@timestamp':{
                                'gte': start_time,
                                'lte': end_time
                            }   
                        }
                        }
                    ]
                }
            }   
        }

        full_queries.append(query)
        client = get_client()
    for q_name, query in zip(q_names,full_queries):
        response = client.search(
                                body = query,
                                index = index_name
        )
        #json_file = json.dumps(response)
        log_out_path = os.path.join(outpath, q_name + '.json')
        with open(log_out_path,'w') as outfile:
            json.dump(response, outfile, indent=4)


    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s','--start_time')
    #if we do not have the end time, use now as the end time
    parser.add_argument('-e','--end_time')
    #flag for logs from day
    parser.add_argument('-d','--day')
    parser.add_argument('-l','--last_hour', action='store_true')
    args = parser.parse_args()

    if args.start_time != None:
        start_time = datetime.strptime(args.start_time, '%Y-%m-%dT%H:%M:%S')
        if args.end_time != None:
            end_time = datetime.strptime(args.end_time, '%Y-%m-%dT%H:%M:%S')
            download_logs_in_time_frame(start_time, end_time)
        else:
            end_time = datetime.utcnow()
            download_logs_in_time_frame(start_time, end_time)

    if args.last_hour == True:
        current_time_utc = datetime.utcnow()
        last_hour_datetime = (current_time_utc - timedelta(hours=1))
        #saves the logs in UTC time no local time to avoid confusion between the reply and the request
        download_logs_in_time_frame(last_hour_datetime, current_time_utc, last_hour=True)

    elif args.day != None:
        #verify that the day is in the correct format
        try:
            day = datetime.strptime(args.day, '%Y-%m-%d')
        except ValueError:
            print('Wrong day format! Use YYYY-MM-DD')
            exit()
        #download every hour of today hour by hour
        start_time = datetime(day.year, day.month, day.day, 0, 0, 0)
        time_inbetween = [start_time + timedelta(hours=i) for i in range(0, 25)]
        for i in range(0, len(time_inbetween)-1):
            download_logs_in_time_frame(time_inbetween[i], time_inbetween[i+1], last_hour=True)

    else:
        print('No arguements!')

