import os
import glob
import argparse

#TODO: for now we just move the files to processed
def preprocess():
    alarms_json_by_receiver = os.path.join('/data', 'raw', 'alarms', 'by_receiver')
    #create vectorstore
    
    return

def move_to_processed(alarms_json_by_receiver, processed_path):
    if not os.path.exists(processed_path):
        os.makedirs(processed_path)
    for file in glob.glob(os.path.join(alarms_json_by_receiver, '*.json')):
        os.rename(file, os.path.join(processed_path, os.path.basename(file)))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    preprocess()